# Project schema

## `project.json`

Required keys:

- `title`: project title
- `source_file`: path to the supplied fiction
- `language`: BCP-47 language tag
- `output_dir`: project output directory
- `visual`: aspect ratio and art-direction constraints
- `tts`: provider, CLI profile, model, format, and sample rate
- `mix`: loudness and true-peak target

## `characters.json`

Each item should contain:

- `id`, `name`, `role`
- `visual_anchors`: age, face, hair, clothing, body, notable traits
- `voice_id`, `voice_direction`, `baseline_rate`, `baseline_pitch`
- `pronunciation_notes`

## `shots.json`

Each item should contain:

- `id`, `scene_id`, `narrative_purpose`
- `characters`, `location`, `action`
- `shot_size`, `camera_angle`, `blocking`
- `time`, `weather`, `lighting`, `aspect_ratio`
- `continuity_anchors`, `prompt`, `image_file`

## `segments.json`

Each item should contain:

- `id`, `shot_id`, `speaker`, `text`
- `voice_id`, `emotion`, `rate`, `pitch`, `instruction`
- `continuity_group`: shared ID for one continuous TTS take
- `audio_file`, `start`, `end`, `duration`

Use `null` for unknown timing before audio is generated. Do not invent timing.

