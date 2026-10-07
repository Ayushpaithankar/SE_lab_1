"""Record 10 seconds of real game frames using deterministic keyboard inputs."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import argparse
import importlib.util
import random
import json
from pathlib import Path
import pygame
import imageio.v2 as imageio
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--game', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--stage', choices=['before', 'after'], required=True)
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('climber', args.game)
game_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_module)
pygame.init()
pygame.display.set_mode((1, 1))
random.seed(37)
game = game_module.Game()
screen = pygame.Surface((game_module.WIDTH, game_module.HEIGHT))
canvas = pygame.Surface((480, 736))
font = pygame.font.Font(None, 23)
class Keys:
    def __init__(self, pressed): self.pressed = pressed
    def __getitem__(self, key): return key in self.pressed

rows = []
target_index = 1
max_height = 0
writer = imageio.get_writer(args.output, fps=60, codec='libx264', quality=8, macro_block_size=16)
try:
    for frame in range(600):
        player = game.player
        if player.on_ground:
            standing_index = game.platforms.index(player.standing_on)
            target_index = min(standing_index + 1, 5)
        target = game.platforms[target_index]
        # Aim at the next platform and jump as soon as a landing is complete.
        desired_x = target.rect.centerx
        pressed = {pygame.K_SPACE}
        if player.rect.centerx < desired_x - 4: pressed.add(pygame.K_RIGHT)
        elif player.rect.centerx > desired_x + 4: pressed.add(pygame.K_LEFT)
        game.update(Keys(pressed))
        max_height = max(max_height, game.height)
        rows.append({'frame': frame, 'height': game.height, 'peak_seen': max_height,
                     'coins': game.coin_score // 50, 'lives': game.lives,
                     'state': game.state, 'camera_y': game.cam_y,
                     'effects': len(getattr(game, 'coin_effects', [])),
                     'platform_3_x': game.platforms[3].rect.x})
        game.draw(screen)
        canvas.fill((12, 16, 26))
        canvas.blit(screen, (0, 64))
        canvas.blit(font.render(f'LAB 4 | {args.stage.upper()} | Automated gameplay', True, (235, 240, 250)), (12, 10))
        canvas.blit(font.render(f'Time {frame / 60:04.1f}s / 10.0s | Best observed: {max_height}m', True, (180, 195, 220)), (12, 34))
        note = 'Height drops after jump peaks; feature hooks empty.' if args.stage == 'before' else 'Peak height held | Color gradient | Motion | Coin sparkles'
        canvas.blit(pygame.font.Font(None, 19).render(note, True, (230, 210, 115)), (12, 714))
        writer.append_data(np.transpose(pygame.surfarray.array3d(canvas), (1, 0, 2)))
        if frame in (90, 300, 599):
            pygame.image.save(canvas, str(Path(args.output).with_name(f'{args.stage}_{frame}.png')))
finally:
    writer.close()
    pygame.quit()
Path(args.output).with_suffix('.json').write_text(json.dumps(rows, indent=2))
print(json.dumps({'frames': len(rows), 'seconds': len(rows)/60, 'peak': max_height,
                  'height_drops': sum(b['height'] < a['height'] for a,b in zip(rows, rows[1:])),
                  'coins': rows[-1]['coins'], 'lives': rows[-1]['lives'],
                  'effect_frames': sum(r['effects'] > 0 for r in rows)}))
