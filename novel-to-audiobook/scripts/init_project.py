#!/usr/bin/env python3
"""Create a safe, empty illustrated-audiobook project from one source file."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


DIRECTORIES = (
    "source", "manifests", "references", "storyboards", "audio/raw",
    "audio/groups", "audio/shots", "audio/sfx", "audio/final",
    "timeline", "reports",
)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: init_project.py /path/to/story /path/to/new-project", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).expanduser().resolve()
    root = Path(sys.argv[2]).expanduser().resolve()
    if not source.is_file():
        print(f"ERROR: source file not found: {source}", file=sys.stderr)
        return 1
    if root.exists() and any(root.iterdir()):
        print(f"ERROR: destination is not empty: {root}", file=sys.stderr)
        return 1

    root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)
    copied = root / "source" / source.name
    shutil.copy2(source, copied)

    project = {
        "title": source.stem,
        "source_file": str(copied.relative_to(root)),
        "language": "zh-CN",
        "output_dir": ".",
        "visual": {
            "aspect_ratio": "16:9",
            "style": "historically grounded illustrated drama",
            "continuity_required": True,
        },
        "tts": {
            "provider": "aliyun-bailian",
            "profile": "token-plan",
            "model": "qwen-audio-3.1-tts-next",
            "format": "wav",
            "sample_rate": 24000,
        },
        "mix": {
            "integrated_lufs": -17.0,
            "true_peak_dbtp": -1.5,
            "text_display_delay_seconds": 0.42,
        },
    }
    (root / "manifests" / "project.json").write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename in ("characters.json", "shots.json", "segments.json", "sfx.json"):
        (root / "manifests" / filename).write_text("[]\n", encoding="utf-8")
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

