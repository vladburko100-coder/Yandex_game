import random

import arcade
import math
import enum

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Bear and cones"
ANIMATION_SPEED = 0.1
GRAVITY = 2


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 1.4
        self.speed = 500
        self.health = 3

        self.idle_texture = arcade.load_texture(
            "data/hero/hero_0.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(0, 2):
            texture = arcade.load_texture(f'data/hero/hero_{i}.png')
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1

        self.is_on_ground = False

        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = 200
        self.center_y = 200

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            # Если не идём, то просто показываем текстуру покоя
            # и поворачиваем её в зависимости от направления взгляда
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update(self, delta_time, keys_pressed):
        """ Перемещение персонажа """
        # В зависимости от нажатых клавиш определяем направление движения
        dx = 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time

        self.center_x += dx

        self.change_y += -GRAVITY

        self.center_y += self.change_y
        if self.center_y <= 200:
            self.change_y = 0
            self.center_y = 200

        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.center_x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.center_x))

        # Проверка на движение
        self.is_walking = dx


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.coin_list = None
        self.player_list = None
        self.texture = arcade.load_texture('data/table.png')
        self.texture1 = arcade.load_texture('data/HP_table/hp3.png')
        self.textures = []
        self.frame = 0
        self.timer = 0

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player = Hero()
        self.player_list.append(self.player)

        self.coin_list = arcade.SpriteList()

        for i in range(12):
            texture = arcade.load_texture(f"data/coins/coin{i}.png")
            self.textures.append(texture)

        coin = arcade.Sprite()
        coin.scale = 1
        coin.texture = self.textures[0]
        coin.center_x = SCREEN_WIDTH // 2
        coin.center_y = SCREEN_HEIGHT // 6 + 10
        self.coin_list.append(coin)

        self.keys_pressed = set()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.center_x, self.center_y // 3.05, 1440, 297))
        arcade.draw_texture_rect(self.texture1, arcade.rect.XYWH(100, 60, 100, 50))
        self.coin_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time, self.keys_pressed)
        self.player_list.update_animation(delta_time)

        self.timer += delta_time
        if self.timer >= ANIMATION_SPEED:
            self.timer -= ANIMATION_SPEED
            self.frame = (self.frame + 1) % 12
            self.coin_list[0].texture = self.textures[self.frame]

        is_collision = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for i in is_collision:
            i.remove_from_sprite_lists()

            for j in range(12):
                texture = arcade.load_texture(f"data/coins/coin{j}.png")
                self.textures.append(texture)

            coin = arcade.Sprite()
            coin.scale = 1
            coin.texture = self.textures[0]
            coin.center_x = random.randint(0 + self.textures[0].width, SCREEN_WIDTH - self.textures[0].width)
            coin.center_y = SCREEN_HEIGHT // 6 + 10
            while (self.player.center_x - self.player.width // 2) <= coin.center_x <= (
                    self.player.center_x + self.player.width // 2):
                coin.center_x = random.randint(0 + self.textures[0].width, SCREEN_WIDTH - self.textures[0].width)
            self.coin_list.append(coin)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.SPACE:
            self.player.change_y = 30

        self.player.center_y += self.player.change_y

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


def setup_game(width=1400, height=900, title="Bear and cones"):
    game = MyGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
