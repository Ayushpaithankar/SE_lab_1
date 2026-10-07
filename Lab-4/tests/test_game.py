"""Regression checks for the assignment tasks and existing gameplay rules."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import random
import unittest
import pygame
import game

class Keys:
    def __init__(self, *pressed): self.pressed = set(pressed)
    def __getitem__(self, key): return key in self.pressed

class HeightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): pygame.init()
    @classmethod
    def tearDownClass(cls): pygame.quit()
    def setUp(self):
        random.seed(37)
        self.g = game.Game()
    def test_best_height_survives_descent(self):
        self.g.player.rect.y = 200
        self.g.update(Keys())
        peak = self.g.height
        self.g.player.rect.y = 400
        self.g.update(Keys())
        self.assertEqual(self.g.height, peak)
        self.assertGreater(peak, 0)
    def test_reset_clears_peak_and_score(self):
        self.g.height = 42
        self.g.coin_score = 50
        self.g.reset()
        self.assertEqual(self.g.height, 0)
        self.assertEqual(self.g.score(), 0)
    def test_coin_score_adds_to_best_height(self):
        self.g.height = 42
        self.g.coin_score = 100
        self.assertEqual(self.g.score(), 142)
    def test_camera_does_not_scroll_down(self):
        self.g.player.rect.y = 100
        self.g.update(Keys())
        camera = self.g.cam_y
        self.g.player.rect.y = 350
        self.g.update(Keys())
        self.assertEqual(self.g.cam_y, camera)

class ColorTests(unittest.TestCase):
    def test_gradient_endpoints_and_middle(self):
        self.assertEqual(game.platform_color(0, 60), (100, 180, 100))
        self.assertEqual(game.platform_color(60, 60), (180, 100, 230))
        self.assertEqual(game.platform_color(30, 60), (140, 140, 165))
    def test_handles_small_and_out_of_range_inputs(self):
        for total in (0, 1, 60):
            for index in (-1, 0, 1, 30, 100):
                color = game.platform_color(index, total)
                self.assertEqual(len(color), 3)
                self.assertTrue(all(isinstance(c, int) and 0 <= c <= 255 for c in color))

class MotionTests(unittest.TestCase):
    def test_only_every_third_platform_moves(self):
        for index in range(61):
            speed = game.moving_platform_speed(index, 60)
            if index > 0 and index % 3 == 0:
                self.assertIn(speed, (1, 2, 3))
            else:
                self.assertEqual(speed, 0)
    def test_ground_is_static_and_mover_bounces(self):
        ground = game.Platform(0, 60, 0, 600, 480, movable=False)
        self.assertEqual(ground.update(), 0)
        mover = game.Platform(60, 60, 100, 300)
        positions = []
        for _ in range(250):
            previous_x = mover.rect.x
            dx = mover.update()
            self.assertEqual(dx, mover.rect.x - previous_x)
            self.assertTrue(mover.bounds[0] <= mover.rect.x <= mover.bounds[1])
            positions.append(mover.rect.x)
        self.assertGreater(len(set(positions)), 30)
        self.assertTrue(any(b < a for a, b in zip(positions, positions[1:])))
    def test_boundary_step_returns_actual_displacement(self):
        mover = game.Platform(60, 60, 100, 300)
        mover.rect.x = mover.bounds[1] - 1
        self.assertEqual(mover.update(), 1)
        self.assertEqual(mover.update(), -3)
    def test_player_is_carried_by_moving_platform(self):
        pygame.init()
        g = game.Game()
        mover = game.Platform(30, 60, 100, 300)
        g.platforms = [mover]
        g.player.rect.centerx = mover.rect.centerx
        g.player.rect.bottom = mover.rect.top
        g.player.on_ground = True
        g.player.standing_on = mover
        old_x = g.player.rect.x
        g.update(Keys())
        self.assertEqual(g.player.rect.x - old_x, 2)
        self.assertIs(g.player.standing_on, mover)
        pygame.quit()

class PickupAndGameplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): pygame.init()
    @classmethod
    def tearDownClass(cls): pygame.quit()
    def setUp(self):
        random.seed(37)
        self.g = game.Game()
    def test_coin_disappears_scores_once_and_starts_effect(self):
        coin = game.Coin(*self.g.player.rect.center)
        self.g.coins = [coin]
        self.g.update(Keys())
        self.assertEqual(self.g.coin_score, 50)
        self.assertEqual(self.g.coins, [])
        self.assertTrue(coin.taken)
        self.assertEqual(len(self.g.coin_effects), 1)
        effect = self.g.coin_effects[0]
        self.assertEqual(effect.score, self.g.score())
        self.assertEqual(len(effect.particles), 12)
        screen = pygame.Surface((480, 640))
        self.g.draw(screen)
        self.g.update(Keys())
        self.assertEqual(self.g.coin_score, 50)
        for _ in range(effect.DURATION): self.g.update(Keys())
        self.assertEqual(self.g.coin_effects, [])
    def test_reset_clears_effects(self):
        self.g.coin_effects = [game.CoinEffect((240, 300), 50)]
        self.g.reset()
        self.assertEqual(self.g.coin_effects, [])
    def test_lands_only_when_falling_from_above(self):
        platform = game.Platform(1, 60, 100, 300)
        player = game.Player(120, 250)
        player.vel_y = 12
        player.update([platform])
        player.update([platform])
        self.assertEqual(player.rect.bottom, platform.rect.top)
        self.assertTrue(player.on_ground)
        player.rect.y = 305
        player.vel_y = -13
        player.update([platform])
        self.assertFalse(player.on_ground)
        self.assertLess(player.vel_y, 0)
    def test_side_contact_does_not_snap_up(self):
        platform = game.Platform(1, 60, 100, 300)
        player = game.Player(90, 290)
        player.vel_y = 4
        player.update([platform])
        self.assertFalse(player.on_ground)
        self.assertGreater(player.rect.bottom, platform.rect.top)
    def test_fall_costs_life_and_preserves_peak(self):
        self.g.height = 99
        self.g.player.rect.y = 800
        self.g.update(Keys())
        self.assertEqual(self.g.lives, 2)
        self.assertEqual(self.g.height, 99)
        self.assertEqual(self.g.player.rect.y, int(self.g.last_safe.y))
        for _ in range(2):
            self.g.player.rect.y = 800
            self.g.update(Keys())
        self.assertEqual(self.g.lives, 0)
        self.assertEqual(self.g.state, 'lose')
    def test_reaching_top_wins(self):
        self.g.player.rect.y = self.g.top_y - 40
        self.g.update(Keys())
        self.assertEqual(self.g.state, 'win')

if __name__ == '__main__': unittest.main()
