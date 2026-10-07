# Verification - Lab 4

Date: 7 October 2026. Environment: Python 3.13.6, Pygame 2.6.1, macOS; automated checks use SDL dummy video/audio drivers.

## Regression tests

`python -m unittest discover -s tests -v` - **16 tests passed**.

- Best height survives descent and falling; reset clears height and score.
- Coin points add to the retained height.
- Camera never scrolls downward.
- Gradient endpoints and midpoint match expected RGB values; small/out-of-range inputs stay valid.
- Only every third non-ground platform moves.
- Ground remains static; movers stay inside bounds and reverse direction.
- Boundary displacement is accurate; standing players are carried correctly.
- Coin pickup removes the coin, scores once, creates 12 particles, draws, and expires.
- Restart clears pickup effects.
- Landing works from above; underside and side contacts do not snap the player upward.
- Falling reduces lives, respawns, and eventually ends in a loss.
- Reaching the top triggers a win.

## Video checks

| Measurement | Before | After |
|---|---:|---:|
| Frames | 600 | 600 |
| Frame rate | 60 FPS | 60 FPS |
| Duration | 10.0 seconds | 10.0 seconds |
| Resolution | 480 x 736 | 480 x 736 |
| Frames where HUD height drops | 131 | 0 |
| Best height observed | 83m | 83m |
| Coins collected | 1 | 1 |
| Frames with coin effect | 0 | 45 |
| Lives remaining | 3 | 3 |

Codec: H.264, yuv420p. The 480 x 640 game area is surrounded by a small recording label and explanatory footer. Sample frames were visually inspected, including the +50 score popup and sparkle burst. Gameplay is automated and clearly labeled in both clips.

The tests and clips verify these behaviors; a student manual-play session is not represented as completed.
