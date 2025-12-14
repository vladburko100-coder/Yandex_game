import arcade
import math
import enum

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Bear and cones"
ANIMATION_SPEED = 0.1


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.sprite_list = None
        self.texture = arcade.load_texture('data/table.png')
        self.texture1 = arcade.load_texture('data/HP_table/hp3.png')
        self.textures = []
        self.frame = 0
        self.timer = 0

    def setup(self):
        self.sprite_list = arcade.SpriteList()

        for i in range(12):
            texture = arcade.load_texture(f"data/coins/coin{i}.png")
            self.textures.append(texture)

        sprite = arcade.Sprite()
        sprite.texture = self.textures[0]
        sprite.center_x = SCREEN_WIDTH // 2
        sprite.center_y = SCREEN_HEIGHT // 4
        sprite.scale = 2
        self.sprite_list.append(sprite)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.center_x, self.center_y // 3.05, 1440, 297))
        arcade.draw_texture_rect(self.texture1, arcade.rect.XYWH(100, 60, 100, 50))
        self.sprite_list.draw()

    def on_update(self, delta_time):
        self.timer += delta_time
        if self.timer >= ANIMATION_SPEED:
            self.timer -= ANIMATION_SPEED
            self.frame = (self.frame + 1) % 12
            self.sprite_list[0].texture = self.textures[self.frame]


def setup_game(width=1400, height=900, title="Bear and cones"):
    game = MyGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
