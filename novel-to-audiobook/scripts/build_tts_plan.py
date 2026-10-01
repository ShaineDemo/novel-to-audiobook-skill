#!/usr/bin/env python3
"""Build deterministic Bailian synthesis jobs from approved segments."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: build_tts_plan.py /absolute/path/to/project", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    project = load(root / "manifests" / "project.json")
    segments = load(root / "manifests" / "segments.json")
    tts = project["tts"]
    grouped: dict[str, list[dict]] = {}
    order: list[str] = []

    for segment in segments:
        key = str(segment.get("continuity_group") or segment["id"])
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(segment)

    jobs = []
    for index, key in enumerate(order, start=1):
        items = grouped[key]
        speakers = {item["speaker"] for item in items}
        voices = {item["voice_id"] for item in items}
        if len(speakers) != 1 or len(voices) != 1:
            raise ValueError(f"continuity group '{key}' mixes speakers or voice IDs")
        jobs.append({
            "job_id": f"tts-{index:03d}",
            "segment_ids": [item["id"] for item in items],
            "speaker": items[0]["speaker"],
            "voice_id": items[0]["voice_id"],
            "text": "\n".join(item["text"].strip() for item in items),
            "rate": items[0].get("rate", 1.0),
            "pitch": items[0].get("pitch", 1.0),
            "instruction": items[0].get("instruction", ""),
            "profile": tts["profile"],
            "model": tts["model"],
            "format": tts["format"],
            "sample_rate": tts["sample_rate"],
            "output": f"audio/groups/tts-{index:03d}.{tts['format']}",
        })

    output = root / "manifests" / "tts-jobs.json"
    output.write_text(json.dumps(jobs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{output}: {len(jobs)} job(s) from {len(segments)} segment(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

