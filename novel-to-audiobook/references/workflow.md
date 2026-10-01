# Workflow

## Phase A — Ingest and structure

1. Extract readable text and keep a source copy unchanged.
2. Read the whole work before creating shots.
3. Build character, scene, shot, speech, and SFX manifests.
4. Record uncertain names, pronunciations, historical details, and continuity risks.

The main output is not a summary. It is a production map that tells downstream image and speech generation what must remain constant and what may change.

## Phase B — Visual generation

1. Create a style frame.
2. Create neutral character references with clear face, hair, clothing, age, and body proportions.
3. Create recurring-location references with stable geometry and direction.
4. Generate shots in narrative order, carrying forward approved references.
5. Review at contact-sheet scale for drift before generating replacements.

Select shots at narrative nodes: new place, character entrance, critical action, reveal, reversal, or emotional turn. A long descriptive passage may share one image; a two-line action can justify its own shot.

## Phase C — Voice production

1. Separate speech by identity.
2. Assign one Voice ID and baseline parameters per identity.
3. Generate 10–20 second casting samples.
4. Lock the cast after approval.
5. Group continuous letters, speeches, and monologues before synthesis.
6. Cut grouped takes into shot-level files only after generation.

Do not use emotional variation as a replacement for casting. A frightened character must still sound like the same person.

## Phase D — Audio post

1. Preserve raw outputs.
2. Trim only obvious leading/trailing silence.
3. Cut long takes at natural pauses.
4. Add short crossfades between adjacent speech assets when needed.
5. Add sparse action SFX.
6. Normalize the assembled mix.
7. Measure final duration and write timeline timestamps.

## Phase E — QA and delivery

Review images, voices, text, timing, and files independently, then test the assembled chapter end to end. Keep regeneration scope narrow: a faulty shot should not trigger a new voice cast; a timing fix should not regenerate an image.

