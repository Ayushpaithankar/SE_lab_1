# Lab 4: task prompts and code review

These are the task briefs used by Codex to organize this run. They are assistant-written briefs, not additional messages written by the student. The submitted chat export records the actual user/assistant conversation.

## Task 1 - best height
Keep the existing height calculation, but make the HUD retain the greatest height reached during a run. Reset it only when starting a new run. Check ascent, descent, scoring, and reset.

Review: `max(self.height, current_height)` preserves the peak; `Game.reset` already initializes it to zero.

## Task 2 - platform color gradient
Implement platform_color(index, total) as a gradual green-to-violet RGB gradient. Treat the top generated index as total, clamp the interpolation, and avoid dividing by zero.

Review: channel interpolation returns integer RGB values. Tests check ground, midpoint, top, and unusual totals.

## Task 3 - moving platforms
Move every third non-ground platform, gradually increasing speed from 1 to 3 pixels per frame with height. Keep the ground static. Verify bounce bounds and carrying the player, including a partial step at the boundary.

Review: integer speeds suit Pygame Rect coordinates. The existing mover now returns its actual displacement at a clamped edge so the rider stays aligned.

## Task 4 - coin pickup feedback
Implement on_coin_collected as a 12-particle sparkle burst and a +50 score popup. Keep effects alive after the collected coin is removed, expire them after 45 frames, and clear them on restart. Preserve single scoring, camera-relative drawing, lives, collision, and win/lose behavior.

Review: the callback attaches the effect to the coin; Game retains it in a separate list before removing collected coins. No external image or sound assets are needed. Regression tests cover pickup, expiry, reset, collision, falling, and victory.
