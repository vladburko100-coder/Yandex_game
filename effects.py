import enum
import math
import random
import arcade


class TVEffect:
    """Класс для эффекта шума старых телевизоров"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scanline_offset = 0

    def update(self):
        """Обновление эффектов"""
        self.scanline_offset += 3
        if self.scanline_offset > self.height:
            self.scanline_offset = 0

    def draw(self):
        """Отрисовка эффектов поверх игры"""
        for _ in range(random.randint(5, 15)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 2)
            arcade.draw_circle_filled(
                x, y, size,
                (255, 255, 255, random.randint(30, 80))
            )


class FaceDirection(enum.Enum):
    """Класс для правильного отображения текстур героя"""
    LEFT = 0
    RIGHT = 1
    UP = 2


class ExplosionParticle(arcade.SpriteCircle):
    """Частица взрыва синего цвета"""

    def __init__(self, x, y):
        color = (0, 191, 255, 255)
        size = random.randint(3, 6)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.alpha = 255
        self.lifetime = random.uniform(0.3, 0.7)
        self.time_alive = 0
        self.scale = 1.0

    def update(self, delta_time):
        self.change_y -= 0.1
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.alpha -= 3
        self.scale_x *= 0.95
        self.scale_y *= 0.95

        self.time_alive += delta_time

        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()
