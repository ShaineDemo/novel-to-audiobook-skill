# Bailian TTS

## Configuration

- Keep credentials in a Bailian CLI profile or environment variable.
- Pass the intended profile explicitly, for example `--config token-plan`.
- Do not assume the globally active profile is the correct account.
- Confirm the model exists in the configured region and subscription before a batch run.

The project may use `qwen-audio-3.1-tts-next` when available. A verified prior production used `qwen-audio-3.0-tts-plus`. Keep the model configurable in `project.json`; do not silently substitute it.

## Command pattern

Use the locally installed CLI help as the authority for exact flags. A typical synthesis job is:

```bash
bl speech synthesize \
  --config token-plan \
  --text-file /absolute/path/segment.txt \
  --model qwen-audio-3.1-tts-next \
  --voice <voice-id> \
  --format wav \
  --sample-rate 24000 \
  --rate 1.0 \
  --pitch 1.0 \
  --instruction '<performance direction>' \
  --out /absolute/path/output.wav
```

Before any `bl` command, follow the installed Bailian Skill protocol, including CLI version and authentication preflight.

## Continuity rule

If adjacent segments share the same `continuity_group`, concatenate their text and synthesize one take. Store the continuous output under `audio/groups/`, then cut shot files with FFmpeg. This avoids voice drift caused by independent sampling.

## Casting rule

Generate short samples before the full run. Compare intelligibility, perceived age, texture, pace, and distance from other cast members. Do not choose voices only because each is pleasant in isolation; the ensemble must remain distinguishable.

