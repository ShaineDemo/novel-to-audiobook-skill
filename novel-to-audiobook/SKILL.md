---
name: novel-to-audiobook
description: "Turn a user-supplied novel or short story into production-ready illustrated audiobook assets: structured scenes and dialogue, consistent storyboard images made with Codex image generation, multi-character Chinese TTS made through Aliyun Bailian, deterministic FFmpeg post-production, and a synchronized timeline. Use when the user asks to make, prototype, revise, or batch an illustrated audiobook or to debug voice consistency, image continuity, or audio timing. Do not use for writing the novel itself or for UI design."
---

# Novel to Audiobook

Build a reproducible asset pipeline, not a one-off demo. Treat the supplied fiction as source material and preserve its meaning, character relationships, chronology, and tone.

## Read first

- Read [workflow.md](references/workflow.md) before starting production.
- Read [project-schema.md](references/project-schema.md) before creating manifests.
- Read [bailian-tts.md](references/bailian-tts.md) before any Bailian call.
- Read [qa-checklist.md](references/qa-checklist.md) before delivery.

## Required input

Require only one novel or short-story file. Accept Markdown, plain text, DOCX, or PDF when text can be extracted reliably. Optional inputs are an art reference, character reference, desired voice direction, target duration, and output aspect ratio.

If optional choices are absent, infer conservative defaults and state them once:

- illustrated audiobook, not video;
- 16:9 storyboard images;
- Chinese historical-drama visual language when supported by the text;
- one stable narrator voice and one stable Voice ID per speaking character;
- sparse action-triggered sound effects, no continuous background bed;
- delivery as images, audio stems, final mix, subtitles, and timeline manifests.

## Production contract

Create a project directory with these durable files before expensive generation:

```text
project/
  source/
  manifests/project.json
  manifests/characters.json
  manifests/shots.json
  manifests/segments.json
  references/
  storyboards/
  audio/raw/
  audio/groups/
  audio/shots/
  audio/sfx/
  audio/final/
  timeline/
  reports/
```

Copy [project.example.json](assets/templates/project.example.json) and [segments.example.json](assets/templates/segments.example.json) as starting points. Do not overwrite user files.

Initialize a clean project with:

```bash
python3 scripts/init_project.py /absolute/path/to/story.md /absolute/path/to/new-project
```

## Workflow

### 1. Structure the content

Read the full source before splitting it. Produce:

- a character bible with identity, relationships, appearance anchors, voice direction, and pronunciation notes;
- a scene list with place, time, weather, spatial continuity, and dramatic purpose;
- a shot list selecting only visually meaningful narrative nodes;
- a speech manifest separating narrator, dialogue, quoted letters, and crowd speech;
- an action-SFX cue list containing only sounds caused by visible or narrated actions.

Do not equate paragraphs with shots. Merge explanatory text when one image can support it. Split when location, speaker, action, information, or emotional direction materially changes.

### 2. Generate storyboard visuals with Codex

Use the available Codex image-generation tool for storyboards. First create and approve stable reference images for recurring characters and locations. Then generate each shot using those references.

Every shot prompt must state: subject, action, blocking, camera distance, camera angle, time, weather, light, environment, aspect ratio, historical constraints, and continuity anchors. Keep fixed traits fixed; vary only expression, pose, lens, framing, and scene lighting.

Never solve continuity by silently redesigning a character. Regenerate only the drifting shot, using the last approved reference.

### 3. Cast and synthesize voices with Bailian

Map one stable Voice ID to each speaking identity. Treat voice as identity and delivery parameters as scene state.

For long letters, monologues, or speeches spanning multiple shots, synthesize one continuous take and cut it afterward. Do not generate the same character separately per picture when vocal continuity matters.

Use the configured Bailian profile explicitly on every command. Never place API keys in manifests, scripts, logs, or the repository. Follow [bailian-tts.md](references/bailian-tts.md).

After approving `segments.json`, create grouped synthesis jobs with:

```bash
python3 scripts/build_tts_plan.py /absolute/path/to/project
```

### 4. Post-produce deterministically

Use FFmpeg for trimming, fades, concatenation, loudness, and action-triggered SFX. Keep source speech stems. Add short sounds only where an action begins, such as opening a letter, stepping onto timber, setting down a cup, or a hull creak.

Default mix target: approximately -17 LUFS integrated and no higher than -1.5 dBTP, unless the destination platform requires otherwise. Favor intelligibility over atmosphere.

### 5. Synchronize and deliver

Derive shot timing from final audio, not from estimated reading speed. Store actual start/end times in the timeline. If text highlighting is shown, apply a small configurable display delay instead of forcing the text to lead the sound.

Validate the project with:

```bash
python3 scripts/validate_project.py /absolute/path/to/project
```

Deliver a concise report of assumptions, generation model/profile, changed files, regeneration risks, and failed or manually reviewed items.

## Decision gates

Pause for user review only at high-leverage points:

1. the character/location visual bible before batch images;
2. a short voice cast sample before batch TTS;
3. one representative mixed scene before assembling the full chapter.

If the user explicitly asks for a fully automatic run, proceed with stated defaults and still preserve these checkpoints as report snapshots.

## Safety and publication

- Work only with content the user supplied or is authorized to transform.
- Do not clone or impersonate a real person's voice without explicit authorization.
- Do not upload source fiction, generated audio, private references, or credentials to a public repository.
- Keep the reusable workflow separate from project-specific assets.
- Do not publish or deploy unless the user explicitly requests it.
