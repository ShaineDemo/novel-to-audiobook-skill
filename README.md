# Novel to Audiobook Skill

Private beta of a Codex Skill that turns a supplied novel or short story into illustrated-audiobook production assets.

It does **not** write the novel and it does **not** build a UI. Its job is the production pipeline:

1. structure characters, scenes, shots, narration, dialogue, and SFX cues;
2. generate consistent storyboard images with Codex image generation;
3. synthesize distinct Chinese character voices through Aliyun Bailian;
4. assemble, normalize, and synchronize the result with FFmpeg.

## Requirements

- Codex desktop or CLI with image generation available
- Python 3.10+
- FFmpeg and FFprobe
- Aliyun Bailian `bl` CLI
- a configured Bailian profile with speech-model access; the examples use a `token-plan` profile

Credentials stay in the Bailian profile or environment. Never commit an API key.

## Install for private testing

Clone this private repository, then copy or symlink the nested skill folder into your Codex skills directory:

```bash
git clone <private-repository-url>
cd novel-to-audiobook-skill
ln -s "$(pwd)/novel-to-audiobook" "$CODEX_HOME/skills/novel-to-audiobook"
```

Restart or reload Codex, then invoke:

```text
$novel-to-audiobook 把这篇短篇小说做成图文有声书生产包。
```

## Private-beta scope

- the repository contains workflow instructions, schemas, templates, and validators;
- it intentionally excludes the original novel, generated storyboards, generated voices, API keys, and account-specific subscription data;
- model and profile are configurable per project;
- publish only after a full chapter passes the included QA checklist.

## Repository layout

```text
novel-to-audiobook/
  SKILL.md
  agents/openai.yaml
  assets/templates/
  references/
  scripts/
```
