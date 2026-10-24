"""Copy an explicit file mapping, preserving source dates. Preview unless --apply."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plain_path(value):
    path = Path(value).expanduser().absolute()
    if '..' in path.parts or '.git' in path.parts:
        raise ValueError(f'Unsupported path: {path}')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f'Symbolic links need a separate migration: {path}')
    return path


def in_skill(path):
    return path.name == 'SKILL.md' or any((p / 'SKILL.md').is_file() for p in path.parents)


def stamp(data, kind, created, updated, migrated):
    text = data.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    lines, body = [], text
    if text.startswith('---' + newline):
        match = re.match(r'\A---\r?\n(.*?)^---[ \t]*(?:\r?\n|$)', text, re.M | re.S)
        if not match:
            raise ValueError('Unclosed front matter')
        lines, body = match.group(1).splitlines(), text[match.end():]
        # Keep the same supported syntax as the aiOS front matter check.
        from common import parse_yaml
        parse_yaml(lines)
    fields = {'type': kind, 'created': created, 'updated': updated, 'migrated': migrated}
    kept = [line for line in lines if line.partition(':')[0] not in fields]
    header = [f'{key}: {value}' for key, value in fields.items()] + kept
    return (newline.join(['---'] + header + ['---', '']) + body).encode('utf-8')


def prepare(mapping, zone):
    now = datetime.now(zone).isoformat(timespec='minutes')
    entries, payloads, destinations, inputs = [], [], set(), set()
    for item in mapping['files']:
        source, destination = plain_path(item['source']), plain_path(item['destination'])
        content_path = plain_path(item.get('content_file', str(source)))
        if not source.is_file() or not content_path.is_file():
            raise ValueError(f'Source or prepared content is not a regular file: {source}')
        if destination.exists() or destination in destinations:
            raise ValueError(f'Destination already exists or repeats: {destination}')
        if any(p.exists() and not p.is_dir() for p in destination.parents):
            raise ValueError(f'Destination parent is not a folder: {destination}')
        destinations.add(destination)
        inputs.update((source, content_path))
        stat = source.stat()
        original = source.read_bytes()
        data = content_path.read_bytes()
        kind = item.get('type')
        fields = {}
        if kind is not None:
            if kind not in ('doc', 'AGENTS.md') or destination.suffix != '.md':
                raise ValueError(f'Invalid document type or extension: {destination}')
            if (destination.name == 'AGENTS.md') != (kind == 'AGENTS.md'):
                raise ValueError(f'Type must match the contract filename: {destination}')
            if in_skill(source) or in_skill(destination):
                raise ValueError(f'Skill files must omit type: {source}')
            birth = getattr(stat, 'st_birthtime', None)
            if birth is None or birth <= 0:
                raise ValueError(f'Creation time unavailable; resolve before importing: {source}')
            fields = {key: datetime.fromtimestamp(value, zone).isoformat(timespec='minutes')
                      for key, value in [('created', birth), ('updated', stat.st_mtime)]}
            data = stamp(data, kind, fields['created'], fields['updated'], now)
        entries.append(dict(source=str(source), destination=str(destination),
                            source_sha256=digest(original), destination_sha256=digest(data),
                            source_mtime_ns=stat.st_mtime_ns,
                            source_birthtime=getattr(stat, 'st_birthtime', None),
                            migrated=now, fields=fields, status='planned'))
        payloads.append((data, stat))
    if not entries:
        raise ValueError('The mapping has no files')
    if destinations & inputs:
        raise ValueError('A destination overlaps a source or prepared content file')
    if any(p in destinations for d in destinations for p in d.parents):
        raise ValueError('A destination file is also a destination folder')
    # Detect skills whose SKILL.md will be created by this same batch.
    skill_dirs = {d.parent for d in destinations if d.name == 'SKILL.md'}
    for entry in entries:
        if entry['fields'] and any(p in skill_dirs for p in Path(entry['destination']).parents):
            raise ValueError('Files in a planned skill package must omit type')
    return entries, payloads, inputs


def run(args):
    mapping_path = plain_path(args.mapping)
    mapping = json.loads(mapping_path.read_text())
    entries, payloads, inputs = prepare(mapping, ZoneInfo(args.zone))
    if not args.apply:
        print(json.dumps({'mode': 'preview', 'files': entries}, indent=2))
        return
    if not args.record:
        raise ValueError('--apply requires --record for the migration record')
    record = plain_path(args.record)
    if record in inputs or record == mapping_path or any(
            record == Path(e['destination']) or record in Path(e['destination']).parents
            or Path(e['destination']) in record.parents for e in entries):
        raise ValueError('The record overlaps migration content')
    record.parent.mkdir(parents=True, exist_ok=True)
    with record.open('x') as log:
        def save():
            log.seek(0)
            json.dump({'mapping': str(mapping_path), 'files': entries}, log, indent=2)
            log.write('\n')
            log.truncate()
            log.flush()
            os.fsync(log.fileno())
        save()
        for entry, (data, stat) in zip(entries, payloads):
            source, destination = Path(entry['source']), Path(entry['destination'])
            if digest(source.read_bytes()) != entry['source_sha256'] or source.stat().st_mtime_ns != stat.st_mtime_ns:
                raise ValueError(f'Source changed during import: {source}')
            plain_path(str(destination))
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as output:
                output.write(data)
            os.chmod(destination, stat.st_mode & 0o777)
            os.utime(destination, ns=(stat.st_atime_ns, stat.st_mtime_ns))
            if digest(destination.read_bytes()) != entry['destination_sha256']:
                raise ValueError(f'Copy verification failed: {destination}')
            entry['status'] = 'copied'
            save()
    print(f'Copied {len(entries)} files. Record: {record}')


def main():
    # Resolve bundled parser without relying on the checkout location.
    for parent in Path(__file__).resolve().parents:
        if (parent / 'hooks' / 'checks' / 'common.py').is_file():
            sys.path.insert(0, str(parent / 'hooks' / 'checks'))
            break
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mapping', help='JSON file with a files list; see references/import-files.md')
    parser.add_argument('--zone', default='America/Los_Angeles', help='Destination front matter time zone')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--record', help='New JSON record path; required with --apply')
    args = parser.parse_args()
    try:
        run(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Migration stopped: {error}\n')


if __name__ == '__main__':
    main()
