import enum
import math
import random
import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UIFlatButton, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.gui.events import UIOnClickEvent

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "CupHead"
ANIMATION_SPEED_COIN = 0.1
GRAVITY = 1.1
FIRE_RATE = 0.2
PLAYER_JUMP_SPEED = 25
COLOR = arcade.color.WHITE
CLICK_SOUND = arcade.load_sound('data/song/change_view.wav')
STYLE_BUTTON = {
    "normal": UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.WHITE,
        bg=(0, 0, 0, 0),
        font_size=43,
    ),
    "hover": UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.BROWN,
        bg=(0, 0, 0, 0),
        font_size=43
    ),
    "press": UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.RED_DEVIL,
        bg=(0, 0, 0, 0),
        font_size=43
    )
}


def create_music_log(filename="all_music.txt"):
    music_info = [
        "Музыка, которая используется в проекте:\n",
        "1. 'Don't Deal With the Devil' - главное меню",
        "2. 'Introduction' - уровень 1",
        "3. 'Die House' - уровень 2",
        "4. 'Level Start' - переход на уровень",
        "5. 'Game Over' - проигрыш",
        "6. 'Winner Sound' - победа",
        "7. 'Timer' - звук таймера перед началом уровня",
        "8. 'Sound Before' - звук перед 'Ready?'",
        "9. 'Go Song' - звук 'Go!'",
        "10. 'Knockout' - победа над боссом",
        "11. 'Change View' - звук кликов в меню",
        "12. 'Pause Response' - звук паузы",
        "13. 'Bomb Sound' - уничтожение бомбы",
        "14. 'Hit Sound' - получение урона",
        "15. 'Player Death' - смерть игрока",
        "16. 'Voicy Coin' - сбор монеты",
        "17. 'Fire Sound' - выстрел игрока",
        "18. 'Jump' - прыжок игрока",
        "19. 'Dash' - рывок игрока",
        "20. 'Landing' - приземление врага",
        "21. 'Enemy Jump' - прыжок врага",
        "22. 'Enemy Hit' - получение урона врагом",
        "23. 'Enemy Hit1' - дополнительный звук урона врага"
    ]

    try:
        with open(filename, mode='w', encoding='utf-8') as f:
            for line in music_info:
                f.write(line + "\n")
    except (ValueError, TypeError, FileNotFoundError) as e:
        exit(0)


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


class MenuView(arcade.View):
    def __init__(self, music_sound=None, is_playing=False, camera_angle=0.0):
        super().__init__()
        self.background = arcade.load_texture('data/others/background_menu.png')
        self.texture_sound_on = arcade.load_texture('data/others/music_on.png')
        self.texture_sound_off = arcade.load_texture('data/others/music_off.png')
        self.background_music = arcade.load_sound("data/song/Don't Deal With the Devil.mp3")

        self.tv_effect = TVEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.camera = arcade.Camera2D()
        self.camera_angle = camera_angle
        self.camera_speed = 0.4
        self.camera_center_x = SCREEN_WIDTH / 2
        self.camera_center_y = SCREEN_HEIGHT / 2

        if music_sound is None:
            self.background_player = self.background_music.play(loop=True, volume=0.3)
        else:
            self.background_player = music_sound

        self.music_is_playing = is_playing

        if not self.music_is_playing:
            self.current_music_texture = self.texture_sound_on
        else:
            self.current_music_texture = self.texture_sound_off

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, align_y=60)
        self.manager.add(self.anchor_layout)

    def on_update(self, delta_time):
        """Обновление кругового движения камеры"""
        self.tv_effect.update()

        jitter_x = random.uniform(-0.05, 0.05)
        jitter_y = random.uniform(-0.05, 0.05)

        self.camera_angle = random.uniform(0, math.pi) * 0.5

        camera_offset_x = math.cos(self.camera_angle)
        camera_offset_y = math.sin(self.camera_angle)

        self.camera.position = (
            self.camera_center_x + camera_offset_x - SCREEN_WIDTH / 2 + self.center_x + 35 + jitter_x,
            self.camera_center_y + camera_offset_y - SCREEN_HEIGHT / 2 + self.center_y + jitter_y
        )

    def setup_widgets(self):
        start = UIFlatButton(text="Start",
                             width=200,
                             height=55,
                             style=STYLE_BUTTON)
        self.box_layout.add(start)

        @start.event("on_click")
        def on_click_start(event: UIOnClickEvent):
            CLICK_SOUND.play()
            self.start_game()

        exit = UIFlatButton(text="Exit",
                            width=170,
                            height=55,
                            style=STYLE_BUTTON)
        self.box_layout.add(exit)

        @exit.event("on_click")
        def on_click_exit(event: UIOnClickEvent):
            CLICK_SOUND.play()
            arcade.stop_sound(self.background_player)
            arcade.exit()

        self.music_button = UITextureButton(texture=self.current_music_texture, x=20, y=20, width=150, height=50,
                                            scale=0.25)
        self.manager.add(self.music_button)

        @self.music_button.event("on_click")
        def on_click_music_button(event: UIOnClickEvent):
            if not self.music_is_playing:
                self.background_player.pause()
                CLICK_SOUND.play()
                self.music_button.texture, self.music_button.texture_hovered = (self.texture_sound_off,
                                                                                self.texture_sound_off)
                self.music_is_playing = True
            else:
                self.background_player.play()
                CLICK_SOUND.play()
                self.music_button.texture, self.music_button.texture_hovered = (self.texture_sound_on,
                                                                                self.texture_sound_on)
                self.music_is_playing = False

    def start_game(self):
        """Функция запуска игры"""
        game_view = Levels(self.background_player, self.music_button.texture, self.music_is_playing, self.camera_angle)
        game_view.setup_widgets()
        self.window.show_view(game_view)
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.camera.use()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.center_x + 35, self.center_y, self.background.width + 30,
                                                  self.background.height))
        self.manager.draw()
        self.tv_effect.draw()


class Levels(arcade.View):
    def __init__(self, music_player, music_texture, is_playing=False, camera_angle=0.0):
        super().__init__()
        self.background = arcade.load_texture('data/others/background_menu.png')
        self.background_player = music_player
        self.music_is_playing = is_playing
        self.music_texture = music_texture
        self.level_start = arcade.load_sound('data/song/level_start.wav')
        self.is_level_start = False

        self.tv_effect = TVEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.transition_active = False
        self.transition_timer = 0
        self.target_level = None
        self.transition_view = None

        self.camera = arcade.Camera2D()
        self.camera_angle = camera_angle
        self.camera_speed = 0.4
        self.camera_center_x = SCREEN_WIDTH / 2
        self.camera_center_y = SCREEN_HEIGHT / 2

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.anchor_layout.add(self.box_layout, align_y=60)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        level_1 = UIFlatButton(text="Level 1",
                               width=270,
                               height=55,
                               style=STYLE_BUTTON)
        self.box_layout.add(level_1)

        @level_1.event("on_click")
        def on_click_level_1(event: UIOnClickEvent):
            self.start_transition_to_level(1)

        level_2 = UIFlatButton(text="Level 2",
                               width=270,
                               height=55,
                               style=STYLE_BUTTON)
        self.box_layout.add(level_2)

        @level_2.event("on_click")
        def on_click_level_2(event: UIOnClickEvent):
            self.start_transition_to_level(2)

        exit = UIFlatButton(text="Exit to menu",
                            width=450,
                            height=55,
                            style=STYLE_BUTTON,
                            x=100,
                            y=800)
        self.box_layout.add(exit)

        @exit.event("on_click")
        def on_click_exit(event: UIOnClickEvent):
            CLICK_SOUND.play()
            game_view = MenuView(self.background_player, self.music_is_playing, self.camera_angle)
            self.window.show_view(game_view)
            self.manager.disable()

    def on_update(self, delta_time):
        """Обновление логики с задержкой"""
        self.tv_effect.update()

        jitter_x = random.uniform(-0.05, 0.05)
        jitter_y = random.uniform(-0.05, 0.05)

        self.camera_angle = random.uniform(0, math.pi) * 0.5

        camera_offset_x = math.cos(self.camera_angle)
        camera_offset_y = math.sin(self.camera_angle)

        self.camera.position = (
            self.camera_center_x + camera_offset_x - SCREEN_WIDTH / 2 + self.center_x + 35 + jitter_x,
            self.camera_center_y + camera_offset_y - SCREEN_HEIGHT / 2 + self.center_y + jitter_y
        )
        if self.transition_active:
            self.transition_timer += delta_time

            if self.transition_timer >= 1.5:
                self.transition_active = False
                self.window.show_view(self.transition_view)
                self.transition_view = None
                self.target_level = None

    def start_transition_to_level(self, level_num):
        """Запускает переход на указанный уровень с задержкой"""
        if not self.transition_active:
            arcade.stop_sound(self.background_player)
            self.level_start.play()
            self.transition_view = MyGame(level=level_num)
            self.transition_view.setup()
            self.transition_active = True
            self.transition_timer = 0
            self.target_level = level_num

            self.manager.disable()

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.center_x + 35, self.center_y, self.background.width + 30,
                                                  self.background.height))
        self.manager.draw()
        self.tv_effect.draw()


class GameOverView(arcade.View):
    def __init__(self, game_view, sound, is_win=False):
        super().__init__()
        self.game_view = game_view
        self.background = arcade.load_texture('data/others/options_menu.png')
        self.game_over_sound = sound
        self.is_win = is_win
        self.game_over_player = self.game_over_sound.play(volume=0.6)
        self.coin_texture = arcade.load_texture('data/coins/coin1.png')
        self.bomb_texture = arcade.load_texture('data/enemy/bomb.png')

        self.tv_effect = TVEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, align_y=-40)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        if self.is_win:
            game_over_text = "YOU WIN!"
            text_color = arcade.color.GOLD
        else:
            game_over_text = "GAME OVER"
            text_color = arcade.color.RED_DEVIL
        self.game_over_text = arcade.Text(
            game_over_text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 150,
            text_color,
            80,
            anchor_x="center",
            anchor_y="center",
            font_name="Gill Sans",
            bold=True,
        )

        self.score_text = arcade.Text(
            f": {self.game_view.total}",
            SCREEN_WIDTH // 2 + 30,
            SCREEN_HEIGHT - 400,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            anchor_y="center",
            font_name="Gill Sans"
        )
        self.bomb_text = arcade.Text(
            f": {self.game_view.bombs_destroyed}",
            SCREEN_WIDTH // 2 + 30,
            SCREEN_HEIGHT - 320,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            anchor_y="center",
            font_name="Gill Sans"
        )

        retry = UIFlatButton(text="Retry",
                             font_size=50,
                             height=55,
                             width=200,
                             style=STYLE_BUTTON)

        @retry.event("on_click")
        def on_click_retry(event):
            CLICK_SOUND.play()
            self.game_over_player.delete()
            games_view = MyGame(level=self.game_view.current_level)
            games_view.setup()
            self.window.show_view(games_view)
            self.manager.disable()

        self.box_layout.add(retry)

        exit = UIFlatButton(text="Exit to menu",
                            font_size=50,
                            height=55,
                            width=450,
                            style=STYLE_BUTTON)

        @exit.event("on_click")
        def on_click_exit(event):
            CLICK_SOUND.play()
            self.game_over_player.delete()
            menu_view = MenuView()
            self.window.show_view(menu_view)
            self.manager.disable()

        self.box_layout.add(exit)

    def on_update(self, delta_time):
        self.tv_effect.update()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(arcade.rect.XYWH(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT),
            (0, 0, 0, 180)
        )
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(self.center_x, self.center_y, self.background.width, self.background.height)
        )
        arcade.draw_texture_rect(self.coin_texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 402, 44, 57))
        self.game_over_text.draw()
        self.score_text.draw()
        if self.game_view.current_level == 1:
            arcade.draw_texture_rect(self.bomb_texture,
                                     arcade.rect.XYWH(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 322, 50, 50))
            self.bomb_text.draw()

        self.manager.draw()
        self.tv_effect.draw()


class PauseView(arcade.View):
    def __init__(self, game_view, background_player):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.background = arcade.load_texture('data/others/pause_menu.png')
        self.pause_response = arcade.load_sound('data/song/pause_response.mp3')
        self.background_player = background_player

        self.tv_effect = TVEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.original_volume = 0.5
        self.pause_volume = 0.1
        self.background_player.volume = self.pause_volume

        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout, align_y=20)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        resume = UIFlatButton(text="Resume",
                              font_size=60,
                              height=55,
                              width=300,
                              font_name='Finlandica Bold',
                              style=STYLE_BUTTON)

        @resume.event("on_click")
        def on_click_resume(event):
            CLICK_SOUND.play()
            self.background_player.volume = self.original_volume
            self.window.show_view(self.game_view)

        self.box_layout.add(resume)

        retry = UIFlatButton(text="Retry",
                             font_size=60,
                             height=55,
                             width=300,
                             font_name='Finlandica Bold',
                             style=STYLE_BUTTON)

        @retry.event("on_click")
        def on_click_retry(event):
            CLICK_SOUND.play()
            self.background_player.volume = self.original_volume
            self.background_player.pause()
            games_view = MyGame(level=self.game_view.current_level)
            games_view.setup()
            self.window.show_view(games_view)
            self.manager.disable()

        self.box_layout.add(retry)

        exit = UIFlatButton(text="Exit to menu",
                            font_size=60,
                            text_color=arcade.color.BLACK,
                            height=55,
                            width=500,
                            font_name='Finlandica Bold',
                            style=STYLE_BUTTON, )

        @exit.event("on_click")
        def on_click_exit(event):
            CLICK_SOUND.play()
            self.background_player.volume = self.original_volume
            self.background_player.pause()
            menu_view = MenuView()
            window.show_view(menu_view)

        self.box_layout.add(exit)

    def on_update(self, delta_time):
        self.tv_effect.update()

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rect_filled(arcade.rect.XYWH(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT),
            (0, 0, 0, 180)
        )
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(self.center_x, self.center_y, self.background.width,
                                                                   self.background.height))
        self.batch.draw()
        self.manager.draw()
        self.tv_effect.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_response.play()
            self.background_player.volume = self.original_volume
            self.window.show_view(self.game_view)


class FaceDirection(enum.Enum):
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


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, speed=1300, damage=1, is_vertical=None, game_view=None):
        super().__init__()
        self.texture = arcade.load_texture('data/hero/hero_bullet.png')
        self.sound_bomb = arcade.load_sound('data/song/bomb_sound.mp3')
        self.change_x = speed
        self.center_x = start_x
        self.center_y = start_y
        self.damage = damage
        self.vertical = is_vertical
        self.game_view = game_view

        self.player = Hero()

    def update(self, delta_time, bomb_list):
        if (self.center_x >= SCREEN_WIDTH or self.center_x <= 0 or
                self.center_y >= SCREEN_HEIGHT or self.center_y <= 0):
            self.remove_from_sprite_lists()

        is_collisions = arcade.check_for_collision_with_list(self, bomb_list)
        for bomb in is_collisions:
            if self.game_view:
                self.game_view.create_explosion_effect(bomb.center_x, bomb.center_y)
                self.game_view.bombs_destroyed += 1
            bomb.remove_from_sprite_lists()
            self.remove_from_sprite_lists()
            arcade.play_sound(self.sound_bomb, volume=0.8)

        if self.vertical:
            self.center_y += self.change_x * delta_time
        else:
            self.center_x += self.change_x * delta_time


class EnemyBomb(arcade.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.idle_texture = arcade.load_texture('data/enemy/bomb.png')
        self.texture = self.idle_texture
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.scale = 1
        self.rotation_speed = 150
        self.angle = 0

    def update(self, delta_time) -> None:
        self.center_y -= self.speed * delta_time

        if self.center_y <= 190:
            self.remove_from_sprite_lists()

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.angle += self.rotation_speed * delta_time


class EnemyGupi(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_texture = arcade.load_texture('data/enemy/gupi/goopy0.png')
        self.prepare_texture = arcade.load_texture('data/enemy/gupi/goopy3.png')
        self.jump_texture = arcade.load_texture('data/enemy/gupi/goopy_jump.png')
        self.hit_texture_1 = arcade.load_texture('data/enemy/gupi/goopy1.png')
        self.hit_texture_2 = arcade.load_texture('data/enemy/gupi/goopy2.png')
        self.dead_texture_1 = arcade.load_texture('data/enemy/gupi/goopy_dead.png')
        self.dead_texture_2 = arcade.load_texture('data/enemy/gupi/goopy_dead2.png')
        self.texture = self.idle_texture
        self.dead_timer = 0
        self.show_dead_texture_2 = True

        self.health = 100
        self.scale = 1.7
        self.center_y = 300
        self.center_x = SCREEN_WIDTH - 250

        self.landing = arcade.load_sound('data/enemy/gupi/landing.mp3')
        self.jump = arcade.load_sound('data/enemy/gupi/jump.mp3')
        self.hit = arcade.load_sound('data/enemy/gupi/hit.mp3')
        self.hit1 = arcade.load_sound('data/enemy/gupi/hit1.mp3')

        self.move_speed = 600
        self.jump_speed = 28
        self.face_direction = FaceDirection.LEFT

        self.state = "idle"
        self.state_timer = 0
        self.timer_hit = 0
        self.change_y = 0
        self.change_x = 0
        self.on_ground = True

        self.left_boundary = 300
        self.right_boundary = SCREEN_WIDTH - 300

        self.hit_timer = 0
        self.hit_timer_change = 0
        self.show_hit = False

        self.idle_timer = 1
        self.player = None

    def update(self, delta_time, bullet_list, player=None) -> None:
        if self.health <= 0:
            self.dead_timer += delta_time
            if self.dead_timer >= 0.4:
                self.show_dead_texture_2 = False
            return

        self.state_timer += delta_time

        if player:
            self.player = player

        if self.show_hit:
            self.hit_timer += delta_time
            if self.hit_timer >= 1:
                self.show_hit = False
                self.hit_timer = 0

        collision_with_bullet = arcade.check_for_collision_with_list(self, bullet_list)
        for bullet in collision_with_bullet:
            if bullet.game_view:
                bullet.game_view.create_explosion_effect(bullet.center_x, bullet.center_y)
            bullet.remove_from_sprite_lists()
            self.health -= 1

            if self.health % 10 == 0:
                self.show_hit = True
                self.hit_timer = 0
                self.original_face_direction = self.face_direction

        if not self.show_hit:
            if self.state == "idle":
                self.change_x = 0
                self.change_y = 0

                self.idle_timer -= delta_time
                if self.idle_timer <= 0:
                    self.state = "preparing"
                    self.state_timer = 0

            elif self.state == "preparing":
                if self.state_timer >= 0.3:
                    self.state = "jumping"
                    self.state_timer = 0
                    self.on_ground = False
                    self.change_y = self.jump_speed
                    self.jump.play()

                    if self.center_x <= self.left_boundary:
                        self.face_direction = FaceDirection.RIGHT
                    elif self.center_x >= self.right_boundary:
                        self.face_direction = FaceDirection.LEFT

                    if self.face_direction == FaceDirection.RIGHT:
                        self.change_x = self.move_speed
                    else:
                        self.change_x = -self.move_speed

            elif self.state == "jumping":
                self.change_y -= GRAVITY

                self.center_x += self.change_x * delta_time
                self.center_y += self.change_y

                if self.center_y <= 300:
                    self.center_y = 300
                    self.change_y = 0
                    self.state = "landing"
                    self.landing.play()
                    self.state_timer = 0

            elif self.state == "landing":
                if self.state_timer >= 0.3:
                    self.state = "idle"
                    self.state_timer = 0
                    self.on_ground = True
                    self.idle_timer = 1

            if self.center_x < self.left_boundary:
                self.face_direction = FaceDirection.RIGHT
            elif self.center_x > self.right_boundary:
                self.face_direction = FaceDirection.LEFT

        if self.show_hit and self.player:
            if self.player.center_x > self.center_x:
                self.face_direction = FaceDirection.RIGHT
            else:
                self.face_direction = FaceDirection.LEFT
        self.center_x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.center_y))

    def update_animation(self, delta_time):
        """Обновление анимации и поворота текстуры"""
        if self.health <= 0:
            if self.show_dead_texture_2:
                self.texture = self.dead_texture_2
            else:
                self.texture = self.dead_texture_1
            return
        if self.show_hit and self.player:
            if self.player.center_x > self.center_x:
                self.face_direction = FaceDirection.RIGHT
            else:
                self.face_direction = FaceDirection.LEFT
        if self.show_hit:
            self.hit_timer_change += delta_time
            if self.hit_timer_change <= 0.3:
                current_texture = self.hit_texture_1
                if not self.hit_sound_played:
                    self.hit.play()
                    self.hit_sound_played = True
                    self.hit1_sound_played = False
            else:
                current_texture = self.hit_texture_2
                if not self.hit1_sound_played:
                    self.hit1.play()
                    self.hit1_sound_played = True
        else:
            self.hit_sound_played = False
            self.hit1_sound_played = False
            self.hit_timer_change = 0
            if self.state == "idle":
                current_texture = self.idle_texture
            elif self.state == "preparing":
                current_texture = self.prepare_texture
            elif self.state == "jumping":
                current_texture = self.jump_texture
            elif self.state == "landing":
                current_texture = self.prepare_texture
            else:
                current_texture = self.idle_texture

        if self.face_direction == FaceDirection.RIGHT:
            self.texture = current_texture.flip_horizontally()
        else:
            self.texture = current_texture
        self.sync_hit_box_to_texture()


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.8
        self.speed = 500
        self.health = 3

        self.idle_texture = arcade.load_texture("data/hero/hero_0.png")
        self.jump_texture = arcade.load_texture('data/hero/hero_3.png')
        self.defeat_texture = arcade.load_texture('data/hero/hero_defeat.png')
        self.texture = self.idle_texture
        self.dash_texture_1 = arcade.load_texture('data/hero/hero_6.png')
        self.dash_texture_2 = arcade.load_texture('data/hero/hero_7.png')
        self.dash_animation_timer = 0
        self.show_dash_texture_2 = False

        self.walk_textures = []
        for i in range(1, 6):
            texture = arcade.load_texture(f'data/hero/hero_{i}.png')
            self.walk_textures.append(texture)

        self.hp_list = []
        for i in range(4):
            hp = arcade.load_texture(f'data/HP_table/hp{i}.png')
            self.hp_list.append(hp)

        self.texture_hp = self.hp_list[self.health]

        self.jump_sound = arcade.load_sound("data/hero/jump.mp3")
        self.attack_sound = arcade.load_sound('data/hero/fire_sound.wav')
        self.hit_sound = arcade.load_sound('data/song/hit_sound.wav')
        self.dash_sound = arcade.load_sound('data/hero/dash.wav')
        self.death_sound = arcade.load_sound('data/hero/player_death.mp3')

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1

        self.timer_hp_table = 1
        self.timer_hp = 0

        self.shoot_timer = 0
        self.is_shooting = False
        self.shoot_duration = 0.2

        self.fire_timer = 0
        self.can_fire = True

        self.is_on_ground = False
        self.is_on_platform = False
        self.is_jump = False
        self.can_double_jump = False
        self.has_double_jump = False

        self.was_on_platform = False
        self.coyote_timer = 0
        self.coyote_time_duration = 0.15
        self.can_coyote_jump = False

        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT

        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 0.5
        self.dash_cooldown = 1.0
        self.dash_cooldown_timer = 0
        self.can_dash = True
        self.dash_speed = 750

        self.invulnerability = False
        self.timer_invulnerability = 0

        self.center_x = 200
        self.center_y = 225

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.is_dashing:
            self.dash_animation_timer += delta_time
            if self.dash_animation_timer >= 0.4:
                self.show_dash_texture_2 = True

            if self.show_dash_texture_2:
                current_dash_texture = self.dash_texture_2
            else:
                current_dash_texture = self.dash_texture_1

            if self.face_direction == FaceDirection.RIGHT:
                self.texture = current_dash_texture
            else:
                self.texture = current_dash_texture.flip_horizontally()
        elif self.is_shooting:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()
        elif self.is_jump or not (self.is_on_ground or self.is_on_platform):
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.jump_texture
            else:
                self.texture = self.jump_texture.flip_horizontally()
        elif self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.face_direction = FaceDirection.LEFT
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.face_direction = FaceDirection.LEFT
                self.texture = self.idle_texture.flip_horizontally()
        if self.health <= 0:
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.defeat_texture
            else:
                self.texture = self.defeat_texture.flip_horizontally()
        self.sync_hit_box_to_texture()

    def update(self, delta_time, keys_pressed, bullet_list, platform_list, boomb_list, game_view, gupi_list):
        """ Перемещение персонажа и стрельба"""
        self.dx = 0
        if self.health <= 0:
            return

        if not self.can_dash:
            self.dash_cooldown_timer += delta_time
            if self.dash_cooldown_timer >= self.dash_cooldown:
                self.can_dash = True
                self.dash_cooldown_timer = 0

        if self.is_dashing:
            self.dash_timer += delta_time
            if self.dash_timer >= self.dash_duration:
                self.stop_dash()

        check_bombs_with_hero = arcade.check_for_collision_with_list(self, boomb_list)
        for bomb in check_bombs_with_hero:
            bomb.remove_from_sprite_lists()
            if self.health > 0:
                arcade.play_sound(self.hit_sound)
                self.health -= 1
                if self.health >= 0:
                    self.texture_hp = self.hp_list[self.health]

        check_gupi_with_hero = arcade.check_for_collision_with_list(self, gupi_list)
        self.sync_hit_box_to_texture()
        for _ in check_gupi_with_hero:
            if not self.invulnerability:
                self.hit_sound.play()
                self.health -= 1
                self.timer_invulnerability = 0
                self.invulnerability = True
                if self.health >= 0:
                    self.texture_hp = self.hp_list[self.health]

        if self.invulnerability:
            self.timer_invulnerability += delta_time
            if self.timer_invulnerability >= 1.0:
                self.invulnerability = False
                self.timer_invulnerability = 0

        if self.health == 1:
            self.timer_hp += delta_time
            if self.timer_hp >= 0.5:
                self.timer_hp = 0
            if self.timer_hp < 0.25:
                self.texture_hp = self.hp_list[1]
            else:
                self.texture_hp = self.hp_list[0]

        if self.health <= 0:
            game_view.show_game_over(is_win=False)
            self.death_sound.play()
            return

        if self.is_on_ground or self.is_on_platform:
            self.was_on_platform = True
            self.coyote_timer = 0
            self.can_coyote_jump = True
        elif self.was_on_platform and not (self.is_on_ground or self.is_on_platform):
            self.coyote_timer += delta_time
            if self.coyote_timer <= self.coyote_time_duration:
                self.can_coyote_jump = True
            else:
                self.can_coyote_jump = False
                self.was_on_platform = False

        if self.is_jump:
            self.can_coyote_jump = False

        if self.is_shooting:
            self.shoot_timer += delta_time
            if self.shoot_timer >= self.shoot_duration:
                self.is_shooting = False
                self.shoot_timer = 0

        if not self.can_fire:
            self.fire_timer += delta_time
            if self.fire_timer >= FIRE_RATE:
                self.can_fire = True
                self.fire_timer = 0

        is_aiming_up = arcade.key.W in keys_pressed or arcade.key.UP in keys_pressed

        if is_aiming_up:
            self.idle_texture = arcade.load_texture('data/hero/hero_0_1.png')
            self.is_aiming_up = True
        else:
            self.idle_texture = arcade.load_texture('data/hero/hero_0.png')
            self.is_aiming_up = False

        if arcade.key.LCTRL in keys_pressed and self.can_fire:
            self.shoot()
            self.can_fire = False
            self.fire_timer = 0
            if is_aiming_up:
                start_x = self.center_x + 29 if self.face_direction == FaceDirection.RIGHT else self.center_x - 29
                start_y = self.center_y + self.height // 3
                bullet = Bullet(start_x, start_y, is_vertical=True, game_view=game_view)
                bullet.texture = bullet.texture.rotate_90()
            else:
                if self.face_direction == FaceDirection.RIGHT:
                    start_x = self.center_x + self.width // 3
                    start_y = self.center_y
                    bullet = Bullet(start_x, start_y, is_vertical=False, game_view=game_view)
                else:
                    start_x = self.center_x - self.width // 3
                    start_y = self.center_y
                    bullet = Bullet(start_x, start_y, -1300, is_vertical=False, game_view=game_view)
            bullet_list.append(bullet)
        if not self.is_dashing:
            if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
                self.dx -= self.speed * delta_time
            if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
                self.dx += self.speed * delta_time

        left_boundary = self.width / 2
        right_boundary = SCREEN_WIDTH - self.width / 2

        at_left_boundary = self.center_x <= left_boundary
        at_right_boundary = self.center_x >= right_boundary

        if at_left_boundary and self.dx < 0:
            self.dx = 0
        elif at_right_boundary and self.dx > 0:
            self.dx = 0

        if self.is_dashing and self.dx == 0:
            if self.face_direction == FaceDirection.RIGHT:
                self.dx = self.speed * 2 * delta_time
            else:
                self.dx = -self.speed * 2 * delta_time

        self.center_x += self.dx
        if not self.is_dashing:
            self.change_y += -GRAVITY
        self.center_y += self.change_y

        self.check_platform_collisions(platform_list)

        if self.center_y <= 225:
            self.change_y = 0
            self.center_y = 225
            self.is_on_ground = True
            self.is_on_platform = False
            self.is_jump = False
            self.can_double_jump = False
            self.has_double_jump = False
            self.was_on_platform = True
            self.can_coyote_jump = True
        else:
            self.is_on_ground = False

        if self.dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif self.dx > 0:
            self.face_direction = FaceDirection.RIGHT

        self.center_x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.center_y))

        self.is_walking = self.dx and not self.is_dashing

    def check_platform_collisions(self, platform_list):
        """Проверяет столкновение с платформами"""
        self.is_on_platform = False

        for platform in platform_list:
            if arcade.check_for_collision(self, platform):
                if self.change_y < 0 and self.bottom >= platform.top - 5:
                    self.bottom = platform.top
                    self.change_y = 0
                    self.is_on_platform = True
                    self.is_jump = False
                    self.can_double_jump = True
                    self.has_double_jump = False
                    return

    def shoot(self):
        """Запуск анимации выстрела"""
        self.is_shooting = True
        self.attack_sound.play()
        self.shoot_timer = 0

    def dash(self):
        """Активация рывка"""
        if self.can_dash and not self.is_dashing:
            self.dash_sound.play()
            self.is_dashing = True
            self.dash_timer = 0
            self.dash_animation_timer = 0
            self.show_dash_texture_2 = False
            self.can_dash = False
            self.dash_cooldown_timer = 0
            self.change_y = 0

    def stop_dash(self):
        """Остановка рывка"""
        self.is_dashing = False
        self.dash_timer = 0


class MyGame(arcade.View):
    def __init__(self, level=None):
        super().__init__()
        self.current_level = level
        self.camera = arcade.Camera2D()

        self.tv_effect = TVEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_list = arcade.SpriteList(use_spatial_hash=True)
        self.bomb_list = arcade.SpriteList(use_spatial_hash=True)
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        self.gupi_list = arcade.SpriteList(use_spatial_hash=True)
        self.explosion_particles = arcade.SpriteList(use_spatial_hash=True)

        self.coin_texture = arcade.load_texture('data/coins/coin1.png')
        self.texture_hp = None

        if level == 1:
            self.texture_background = arcade.load_texture('data/others/background_2.jpeg')
            self.platform_texture = 'data/others/platform_1.png'
            self.background_music = arcade.load_sound('data/song/introduction.mp3')
            self.texture_table = arcade.load_texture('data/others/table.png')

            self.level_timer = 90.0
            self.timer_running = False
        elif level == 2:
            self.knockout_texture = arcade.load_texture('data/others/knockout.png')
            self.texture_background = arcade.load_texture('data/others/background.jpg')
            self.platform_texture = 'data/others/platform_0.png'
            self.background_music = arcade.load_sound('data/song/Die House.mp3')
            self.texture_table = arcade.load_texture('data/others/table.png')

        self.sound_coin = arcade.load_sound("data/coins/voicy_coin.mp3")
        self.background_player = None
        self.sound_before = arcade.load_sound('data/song/sound_before.wav')
        self.has_sound_before = True
        self.go_sound = arcade.load_sound('data/song/go_song.wav')
        self.has_go_sound = True
        self.go_sound_timer = 0
        self.pause_response = arcade.load_sound('data/song/pause_response.mp3')
        self.game_over_sound = arcade.load_sound('data/song/game_over.mp3')
        self.winner_sound = arcade.load_sound('data/song/winner_sound.mp3')
        self.timer_sound = arcade.load_sound('data/song/timer.wav')
        self.knockout = arcade.load_sound('data/song/knockout.wav')

        self.countdown_active = True
        self.countdown_value = 4
        self.countdown_timer = 0
        self.game_started = False
        self.game_over = False

        self.textures = []
        self.frame = 0
        self.timer = 0
        self.total = 0

        self.bombs_destroyed = 0
        self.game_over_timer = 0

        self.gupi_death_timer = None
        self.show_knockout = None

    def create_explosion_effect(self, x, y):
        """Создает эффект синего взрыва"""
        for _ in range(30):
            particle = ExplosionParticle(x, y)
            self.explosion_particles.append(particle)

    def setup(self):
        self.batch = Batch()
        self.batch_before = Batch()
        self.batch_timer = Batch()
        self.total_coins = arcade.Text(f': {str(self.total)}', SCREEN_WIDTH - 100, 45, COLOR,
                                       25,
                                       font_name='Gill Sans',
                                       batch=self.batch)

        if self.current_level == 1:
            self.timer_text = arcade.Text('', SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, arcade.color.WHITE,
                                          30, anchor_x="center", batch=self.batch_timer)

        self.player = Hero()
        self.player_list.append(self.player)

        self.texture_hp = self.player.texture_hp

        for i in range(12):
            texture = arcade.load_texture(f"data/coins/coin{i}.png")
            self.textures.append(texture)

        coin = arcade.Sprite()
        coin.scale = 1.3
        coin.texture = self.textures[0]
        coin.center_x = SCREEN_WIDTH // 2
        coin.center_y = SCREEN_HEIGHT // 5.1
        self.coin_list.append(coin)

        self.keys_pressed = set()

        self.platform_create()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.platform_list,
            gravity_constant=GRAVITY
        )
        if self.current_level == 2:
            self.gupi = EnemyGupi()
            self.gupi_list.append(self.gupi)

        self.countdown_active = True
        self.countdown_value = 4
        self.countdown_timer = 0
        self.game_started = False
        self.game_over = False

        self.last_stage = None

        self.is_win = None

        self.timer_bomb = 0.0
        self.timer_bomb_end = 0.0

        self.bombs_destroyed = 0

        self.gupi_death_timer = None
        self.show_knockout = None

        self.has_go_sound = True
        self.go_sound_timer = 0

        self.has_sound_before = True

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        arcade.draw_texture_rect(self.texture_background,
                                 arcade.rect.XYWH(self.center_x, self.center_y + 150, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.texture_table, arcade.rect.XYWH(self.center_x, 150, 1440, 297))
        arcade.draw_texture_rect(self.player.texture_hp, arcade.rect.XYWH(100, 60, 100, 50))
        arcade.draw_texture_rect(self.coin_texture, arcade.rect.XYWH(SCREEN_WIDTH - 120, 60, 44, 57))
        self.coin_list.draw()
        self.platform_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.gupi_list.draw()
        if self.show_knockout and self.game_over_timer < 0.3:
            arcade.draw_texture_rect(self.knockout_texture,
                                     arcade.rect.XYWH(self.center_x, self.center_y, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bomb_list.draw()
        self.batch.draw()
        self.explosion_particles.draw()
        self.tv_effect.draw()

        if self.current_level == 1 and self.game_started and not self.game_over:
            minutes = int(self.level_timer) // 60
            seconds = int(self.level_timer) % 60
            timer_str = f"{minutes:02d}:{seconds:02d}"

            if self.level_timer <= 10:
                color = arcade.color.RED
            elif self.level_timer <= 30:
                color = arcade.color.YELLOW
            else:
                color = arcade.color.WHITE

            timer = arcade.Text(timer_str, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, color,
                                30, anchor_x="center", font_name="Gill Sans", bold=True, batch=self.batch_timer)
            self.batch_timer.draw()

        if self.countdown_active:
            arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                                    (0, 0, 0, 100))
            current_stage = None
            if self.countdown_value > 1:
                current_stage = f"number_{self.countdown_value - 1}"
                self.text = str(self.countdown_value - 1)
                self.color = arcade.color.RED
                self.font_size = 200
            elif self.countdown_value == 1:
                current_stage = "ready"
                self.text = "Ready?"
                self.color = arcade.color.YELLOW
                self.font_size = 120

            if hasattr(self, 'last_stage') and self.last_stage != current_stage:
                self.timer_sound.play()

            self.last_stage = current_stage

            number = arcade.Text(
                self.text,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                self.color,
                self.font_size,
                anchor_x="center",
                anchor_y="center",
                font_name="Gill Sans",
                bold=True,
                batch=self.batch_before
            )
            self.batch_before.draw()

    def on_update(self, delta_time):
        self.tv_effect.update()
        if self.game_over:
            self.game_over_timer += delta_time
            if self.game_over_timer >= 2:
                if self.is_win:
                    sound_to_play = self.winner_sound
                else:
                    sound_to_play = self.game_over_sound

                game_over_view = GameOverView(self, sound_to_play, is_win=self.is_win)
                self.window.show_view(game_over_view)
            return

        if self.countdown_active:
            self.countdown_timer += delta_time

            if self.countdown_value == 2 and self.has_sound_before:
                self.sound_before.play()
                self.has_sound_before = False

            if self.countdown_timer >= 1:
                self.countdown_timer = 0
                self.countdown_value -= 1

                if self.countdown_value <= 0:
                    self.go_sound.play()
                    self.countdown_active = False
                    self.game_started = True
                    self.background_player = arcade.play_sound(self.background_music, loop=True, volume=0.5)
                    if self.current_level == 1:
                        self.timer_running = True
            return

        if self.game_started and not self.game_over:
            self.explosion_particles.update(delta_time)
            if self.current_level == 1 and self.timer_running:
                self.level_timer -= delta_time
                if self.level_timer <= 0:
                    self.level_timer = 0
                    self.timer_running = False
                    self.show_game_over(is_win=True)
                    return

            if not self.player.is_dashing:
                self.physics_engine.update()
            self.player_list.update(delta_time, self.keys_pressed, self.bullet_list, self.platform_list, self.bomb_list,
                                    self, self.gupi_list)
            self.player_list.update_animation(delta_time)
            self.bullet_list.update(delta_time, self.bomb_list)
            self.bomb_list.update(delta_time)
            self.gupi_list.update(delta_time, self.bullet_list, self.player)
            self.gupi_list.update_animation(delta_time)

            for bomb in self.bomb_list:
                bomb.update_animation(delta_time)

            if self.current_level == 1:
                self.timer_bomb += delta_time
                self.timer_bomb_end += delta_time
                if self.timer_bomb >= 0.2:
                    self.timer_bomb = 0.0
                    bomb = EnemyBomb(random.randint(100, SCREEN_WIDTH - 100), SCREEN_HEIGHT, 500)
                    bomb.center_y = SCREEN_HEIGHT + bomb.height
                    self.bomb_list.append(bomb)

            self.timer += delta_time
            if self.timer >= ANIMATION_SPEED_COIN:
                self.timer -= ANIMATION_SPEED_COIN
                self.frame = (self.frame + 1) % 12
                self.coin_list[0].texture = self.textures[self.frame]

            is_collision = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for i in is_collision:
                self.total += 1
                self.sound_coin.play()
                self.total_coins = arcade.Text(f': {str(self.total)}', SCREEN_WIDTH - 100, 45, COLOR,
                                               25,
                                               font_name='Gill Sans',
                                               batch=self.batch)
                i.remove_from_sprite_lists()

                for j in range(12):
                    texture = arcade.load_texture(f"data/coins/coin{j}.png")
                    self.textures.append(texture)

                coin = arcade.Sprite()
                coin.scale = 1.3
                coin.texture = self.textures[0]
                coin.center_x = random.randint(0 + self.textures[0].width, SCREEN_WIDTH - self.textures[0].width)
                coin.center_y = SCREEN_HEIGHT // 5.1

                for _ in range(10):
                    if (self.player.center_x - self.player.width // 2 - 120) <= coin.center_x <= (
                            self.player.center_x + self.player.width // 2 + 120):
                        coin.center_x = random.randint(int(coin.width // 2), SCREEN_WIDTH - int(coin.width // 2))
                self.coin_list.append(coin)

        if self.current_level == 2:
            if self.gupi.health <= 0 and not self.game_over:
                self.gupi.center_y = 350
                if self.gupi_death_timer is None:
                    self.show_knockout = True
                    self.gupi_death_timer = 0
                    self.knockout.play()
                self.gupi_death_timer += delta_time
                if self.gupi_death_timer >= 0.5:
                    self.show_game_over(is_win=True)

    def show_game_over(self, is_win=False):
        """Показать экран Game Over"""
        if not self.game_over:
            self.background_player.pause()
            self.game_over = True
            self.game_over_timer = 0.0
            self.is_win = is_win
            if not self.is_win:
                self.player.texture_hp = arcade.load_texture('data/HP_table/hp_dead.png')

    def platform_create(self):
        """Создание плит"""
        start_x = random.randint(150, 400)
        start_y = random.randint(350, 450)

        patterns = [
            [0, 1, -1],
            [0, -1, 1],
        ]

        pattern = random.choice(patterns)

        max_jump_height = 300

        for i in range(3):
            platform = arcade.Sprite(self.platform_texture, scale=1.0)

            if i == 0:
                platform.center_x = start_x
            else:
                prev_platform = self.platform_list[i - 1]
                distance_x = random.randint(400, 550)
                platform.center_x = prev_platform.center_x + distance_x

            platform.center_x += random.randint(-40, 40)

            if i == 0:
                platform.center_y = max(350, start_y)
            else:
                height_change = random.randint(150, 250)
                direction = pattern[i]
                prev_platform = self.platform_list[i - 1]

                proposed_y = prev_platform.center_y + (height_change * direction)

                if direction == 1:
                    if proposed_y - prev_platform.center_y > max_jump_height:
                        proposed_y = prev_platform.center_y + max_jump_height

                platform.center_y = max(350, proposed_y)

            platform.center_x = max(100, min(SCREEN_WIDTH - 100, int(platform.center_x)))

            max_allowed_height = 350 + (i * 200)

            if platform.center_y > max_allowed_height:
                platform.center_y = max_allowed_height

            absolute_max_height = 650
            if platform.center_y > absolute_max_height:
                platform.center_y = absolute_max_height

            if i > 0:
                prev_platform = self.platform_list[i - 1]

                if platform.center_y > prev_platform.center_y:
                    height_diff = platform.center_y - prev_platform.center_y
                    if height_diff > max_jump_height:
                        platform.center_y = prev_platform.center_y + max_jump_height

            if i > 0:
                prev_platform = self.platform_list[i - 1]
                min_vertical_distance = 120

                if abs(platform.center_y - prev_platform.center_y) < min_vertical_distance:
                    if platform.center_y > prev_platform.center_y:
                        platform.center_y = prev_platform.center_y + min_vertical_distance
                    else:
                        platform.center_y = prev_platform.center_y - min_vertical_distance

            if i > 0:
                prev_platform = self.platform_list[i - 1]
                distance_x_between = abs(platform.center_x - prev_platform.center_x)

                if distance_x_between < 380:
                    if platform.center_x > prev_platform.center_x:
                        platform.center_x = prev_platform.center_x + 380
                    else:
                        platform.center_x = prev_platform.center_x - 380
                elif distance_x_between > 650:
                    if platform.center_x > prev_platform.center_x:
                        platform.center_x = prev_platform.center_x + 650
                    else:
                        platform.center_x = prev_platform.center_x - 650

            if platform.center_y < 395:
                platform.center_y = 395

            self.platform_list.append(platform)

    def on_key_press(self, key, modifiers):
        if not self.game_started or self.game_over:
            return
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            self.pause_response.play()
            pause_view = PauseView(self, self.background_player)
            self.window.show_view(pause_view)
        if key == arcade.key.SPACE and not self.player.is_dashing:
            if ((self.player.is_on_ground or self.player.is_on_platform or self.player.can_coyote_jump)
                    and not self.player.is_jump):
                self.player.jump_sound.play(volume=2)
                self.player.change_y = PLAYER_JUMP_SPEED
                self.player.is_jump = True
                self.player.is_on_ground = False
                self.player.is_on_platform = False
                self.player.can_double_jump = True
                self.player.has_double_jump = False
                self.player.can_coyote_jump = False
                self.player.was_on_platform = False
            elif self.player.can_double_jump and not self.player.has_double_jump and not (
                    self.player.is_on_ground or self.player.is_on_platform):
                self.player.jump_sound.play(volume=2)
                self.player.can_double_jump = False
                self.player.has_double_jump = True
                self.player.change_y = PLAYER_JUMP_SPEED * 0.7
        if key == arcade.key.LSHIFT:
            self.player.dash()

    def on_key_release(self, key, modifiers):
        if not self.game_started or self.game_over:
            return
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


if __name__ == '__main__':
    create_music_log()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
