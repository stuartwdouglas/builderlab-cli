#!/usr/bin/env python3
"""Build a dependency-free Hello World artifact for bl apps deploy."""

import argparse
import gzip
import io
import json
from pathlib import Path
import re
import tarfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--version-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,46}[a-z0-9])?", args.app_id):
        parser.error("--app-id must be a DNS-safe lowercase label of at most 48 characters")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", args.version_id):
        parser.error("--version-id must contain 1–128 letters, numbers, dots, hyphens, or underscores")

    manifest = {
        "schema": "hotpod.manifest.v1",
        "app": {"app_id": args.app_id, "name": "Hello World"},
        "version": {
            "version_id": args.version_id,
            "compatibility_date": "2026-09-29",
        },
        "runtime": {"profile": "fetch-js", "entrypoint": "server/index.mjs"},
        "bindings": [
            {"name": "ASSETS", "type": "assets"},
            {"name": "HOTPOD", "type": "hotpod"},
        ],
    }
    files = {
        "hotpod.manifest.json": json.dumps(manifest, indent=2).encode() + b"\n",
        "server/index.mjs": (Path(__file__).parent / "server/index.mjs").read_bytes(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for name, data in files.items():
                    entry = tarfile.TarInfo(name)
                    entry.size = len(data)
                    entry.mode = 0o644
                    archive.addfile(entry, io.BytesIO(data))
    print(args.output)


if __name__ == "__main__":
    main()
