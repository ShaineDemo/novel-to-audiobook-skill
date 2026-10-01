#!/usr/bin/env python3
"""Validate a novel-to-audiobook project without modifying it."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {path}: {exc}") from None


def require(mapping, keys, label, errors):
    for key in keys:
        if key not in mapping:
            errors.append(f"{label}: missing key '{key}'")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_project.py /absolute/path/to/project", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 1

    try:
        project = load_json(root / "manifests" / "project.json")
        segments = load_json(root / "manifests" / "segments.json")
        shots = load_json(root / "manifests" / "shots.json")
        characters = load_json(root / "manifests" / "characters.json")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    require(project, ["title", "source_file", "language", "output_dir", "visual", "tts", "mix"], "project.json", errors)
    if isinstance(project.get("tts"), dict):
        require(project["tts"], ["provider", "profile", "model", "format", "sample_rate"], "project.json.tts", errors)

    for name, value in [("segments.json", segments), ("shots.json", shots), ("characters.json", characters)]:
        if not isinstance(value, list) or not value:
            errors.append(f"{name}: expected a non-empty array")

    character_names = {c.get("name") for c in characters if isinstance(c, dict)}
    seen_ids: set[str] = set()
    groups: dict[str, list[dict]] = {}
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            errors.append(f"segments.json[{index}]: expected object")
            continue
        require(segment, ["id", "shot_id", "speaker", "text", "voice_id", "continuity_group"], f"segment {index}", errors)
        sid = segment.get("id")
        if sid in seen_ids:
            errors.append(f"segments.json: duplicate id '{sid}'")
        if sid:
            seen_ids.add(sid)
        speaker = segment.get("speaker")
        if speaker not in character_names and speaker not in {"Narrator", "旁白"}:
            warnings.append(f"segment {sid}: speaker '{speaker}' is not in characters.json")
        group = segment.get("continuity_group")
        if group:
            groups.setdefault(str(group), []).append(segment)

    for group, items in groups.items():
        voices = {item.get("voice_id") for item in items}
        speakers = {item.get("speaker") for item in items}
        if len(voices) > 1 or len(speakers) > 1:
            errors.append(f"continuity group '{group}' mixes speakers or voice IDs")

    source = root / str(project.get("source_file", ""))
    if not source.is_file():
        warnings.append(f"source file does not exist: {source}")
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            warnings.append(f"optional runtime not found: {binary}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: {len(segments)} segments, {len(shots)} shots, {len(characters)} characters, {len(groups)} continuity group(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

