# Lab 4 - Climber Repair

Student: Ayush Paithankar | PES1UG24CS104 | Assigned repository: 37_climber

Source: [SETAPESU26/37_climber](https://github.com/SETAPESU26/37_climber), cloned at commit `63be6dfa1518997439d02cf661c57762d028da49`.

## Completed tasks

1. **Best height:** the HUD keeps the greatest height reached during the run. It clears on restart.
2. **Platform colors:** platforms gradually blend from green at ground level to violet at the top.
3. **Moving platforms:** every third non-ground platform oscillates horizontally at 1-3 pixels per frame. Rider displacement uses the platform's actual movement at boundaries.
4. **Coin feedback:** collecting a coin creates 12 sparkles and a +50 score popup for 45 frames. Coins disappear and score once; effects clear on reset.

Each task has a separate commit in this repository.

## Run

Requires Python 3.10 or newer.

```bash
cd Lab-4
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python game.py
```

On Windows, activate with `.venv\Scripts\activate`.

Controls: A/Left and D/Right move, Space/W/Up jump, R restarts, and closing the window exits.

## Submission files

- [Before gameplay](videos/before.mp4)
- [After gameplay](videos/after.mp4)
- [Updated code](game.py)
- [Chat/LLM page](https://chatgpt.com/s/cx_6ac5e8f42d2c81919aecfd7d098a687f)
- [Chat history PDF](CHAT_HISTORY.pdf) and [text version](CHAT_HISTORY.md)
- [Task briefs and code review notes](PROMPTS.md)
- [Verification report](VALIDATION.md)
- [Original assignment README](ASSIGNMENT_README.md)

## About the recordings

Both clips contain exactly 600 game-rendered frames at 60 FPS: 10 seconds each, encoded as H.264 MP4. Codex recorded a seeded game using repeatable keyboard inputs; these are **automated gameplay demonstrations**, not a recording of the student manually playing. No game state or score was altered by the recording harness. The before clip was produced from the untouched original code before changes. The same seed and controller were used for the final clip.

The original height decreases on 131 frames; the final height never decreases. The final clip also shows oscillating platforms and 45 frames of coin pickup feedback. Full frame measurements are available in `videos/before.json` and `videos/after.json`.

The game uses no external art or sound assets.

## Verify or reproduce

```bash
python -m unittest discover -s tests -v
python -m pip install -r tools/requirements-recording.txt
python tools/record_gameplay.py --game tools/original_game.py --output videos/before.mp4 --stage before
python tools/record_gameplay.py --game game.py --output videos/after.mp4 --stage after
```

The recorder uses SDL's offscreen rendering driver and the game's original update/draw methods. It sets random seed 37 and supplies movement/jump keys for 600 frames.

The task briefs in PROMPTS.md were written by the assistant to organize the work. CHAT_HISTORY contains the actual user/assistant conversation through its export point. Review the four changes and try the controls before presenting the assignment.
