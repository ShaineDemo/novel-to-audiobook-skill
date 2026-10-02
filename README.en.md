# Novel to Illustrated Audiobook Skill

[简体中文](README.md) | [English](README.en.md)

> Private beta: turn an existing novel or short story into a production-ready package of illustrated audiobook assets.

This skill does not write the novel. It starts with fiction supplied by the user, uses Codex to structure the content and generate consistent storyboard images, uses Alibaba Cloud Model Studio (Bailian) for multi-character Chinese speech, and uses FFmpeg for trimming, assembly, loudness normalization, action-triggered sound effects, and timeline synchronization.

## Preview

[![Illustrated audiobook UI preview](docs/assets/ui-preview.png)](docs/index.html)

The repository includes an interactive UI demo with:

- play, pause, seek, and playback-speed controls;
- previous/next scene navigation and keyboard shortcuts;
- synchronized storyboard images, speaker information, text, and audio;
- responsive desktop and mobile layouts;
- keyboard focus, accessibility labels, and reduced-motion support.

### Run the interactive demo locally

After cloning the repository, run:

```bash
python3 -m http.server 8080 --directory docs
```

Then open:

```text
http://127.0.0.1:8080/
```

If the repository is made public later, the existing `docs/` directory can be used directly as the source for GitHub Pages.

## What it does

The workflow performs four transformations:

1. **Structure the content**: identify characters, locations, actions, narration, dialogue, and sound-effect cues.
2. **Generate storyboards**: select meaningful story beats and create visually consistent sequential images.
3. **Create voices**: assign a stable voice to the narrator and every character, then adjust delivery without changing vocal identity.
4. **Post-produce audio**: assemble speech, add sparse action-triggered sound effects, normalize loudness, and generate subtitles and a synchronized timeline.

```text
Novel or short story
   ↓
Characters / scenes / actions / dialogue
   ↓
Sequential storyboard images + multi-character speech
   ↓
Audio post-production + subtitles + shot timeline
   ↓
Illustrated audiobook asset package
```

## Platforms and tools

- **Codex**: reads the story, structures the narrative, generates storyboard images, manages project files, and orchestrates the workflow.
- **Alibaba Cloud Model Studio (Bailian)**: generates narrator and character tracks through the `bl` CLI and a Chinese TTS model.
- **FFmpeg / FFprobe**: trims and concatenates audio, applies fades, normalizes loudness, and performs technical checks.
- **Python 3.10+**: initializes projects, creates TTS plans, and validates deliverables.

Codex and Bailian are separate products with separate subscriptions and billing. Bailian credentials must stay in a local profile or environment variable. Never place API keys in the repository, scripts, logs, or project manifests.

## Installation

> This repository is currently a private beta. You need repository access and a locally authenticated GitHub account before installation.

### Option 1: Install from Codex (recommended)

Enter this in a Codex conversation:

```text
$skill-installer install https://github.com/ShaineDemo/novel-to-audiobook-skill/tree/main/novel-to-audiobook
```

Reload Codex after installation, then invoke the skill with:

```text
$novel-to-audiobook Turn this short story into an illustrated audiobook asset package.
```

### Option 2: Manual installation on macOS or Linux

```bash
git clone https://github.com/ShaineDemo/novel-to-audiobook-skill.git
cd novel-to-audiobook-skill

SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$SKILLS_DIR"
ln -s "$(pwd)/novel-to-audiobook" "$SKILLS_DIR/novel-to-audiobook"
```

If a skill with the same name already exists at the destination, inspect it for local changes before removing or renaming it. Do not overwrite unknown files.

### Option 3: Manual installation on Windows PowerShell

```powershell
git clone https://github.com/ShaineDemo/novel-to-audiobook-skill.git
Set-Location novel-to-audiobook-skill

$skillsDir = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME "skills"
} else {
  Join-Path $HOME ".codex\skills"
}

New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -Recurse .\novel-to-audiobook (Join-Path $skillsDir "novel-to-audiobook")
```

Reload Codex, then invoke the skill with:

```text
$novel-to-audiobook Turn this short story into an illustrated audiobook asset package.
```

### Updating

For a manual clone, update the repository with:

```bash
cd /path/to/novel-to-audiobook-skill
git pull --ff-only
```

A symlink installation uses the updated files immediately. A copied installation must be copied again after updating.

## Minimum input

You only need a complete novel or short story. Supported inputs include Markdown, plain text, and DOCX or PDF files from which the text can be extracted reliably.

Optional inputs include:

- art-direction references;
- character references;
- voice preferences;
- target duration;
- output aspect ratio.

When these are omitted, the skill uses conservative defaults and asks for approval at three high-leverage checkpoints: character appearance, voice casting, and one representative mixed scene.

## Quick start

Initialize a project:

```bash
python3 novel-to-audiobook/scripts/init_project.py \
  /absolute/path/to/story.md \
  /absolute/path/to/new-project
```

After reviewing `manifests/segments.json`, build the Bailian synthesis plan:

```bash
python3 novel-to-audiobook/scripts/build_tts_plan.py \
  /absolute/path/to/new-project
```

After generation, validate the project:

```bash
python3 novel-to-audiobook/scripts/validate_project.py \
  /absolute/path/to/new-project
```

## Deliverables

```text
project/
├── storyboards/        # Sequential storyboard images
├── audio/
│   ├── raw/            # Raw character speech returned by Bailian
│   ├── groups/         # Continuous takes for long dialogue or narration
│   ├── shots/          # Audio cut to individual shots
│   ├── sfx/            # Action-triggered sound effects
│   └── final/          # Final mixes
├── timeline/           # Subtitles, shot order, and measured timing
├── manifests/          # Characters, shots, dialogue, and project metadata
└── reports/            # Automated checks and manual-review records
```

These files can be imported into CapCut, Premiere Pro, or another editor, or used to build an interactive illustrated-reading experience like the included demo.

## Production principles

- A paragraph is not automatically a shot; only visualize meaningful story beats.
- Approve stable character and location references before batch image generation.
- Keep one Voice ID for each character.
- Generate long letters, monologues, and speeches as one continuous take, then cut them by shot.
- Do not run a constant ambience bed by default; add short sounds only when visible actions occur.
- Derive shot timing from the final audio instead of estimating reading speed.

## Repository structure

```text
.
├── README.md                    # Chinese documentation (default)
├── README.en.md                 # English documentation
├── docs/                        # Interactive UI demo; GitHub Pages-ready
└── novel-to-audiobook/
    ├── SKILL.md                 # Skill entry point
    ├── agents/openai.yaml       # Codex UI and invocation metadata
    ├── assets/templates/        # Project manifest templates
    ├── references/              # Workflow, Bailian, schema, and QA guidance
    └── scripts/                 # Project initialization, TTS planning, and validation
```

## Private-beta scope

- This repository currently validates the workflow, project structure, voice continuity, and UI demo.
- It does not contain API keys, private source fiction, or account information.
- The demo uses selected short excerpts and compressed assets rather than a complete production project.
- Before public release, review sample-asset rights, current Bailian model names, and subscription requirements.
