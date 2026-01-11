import random
import arcade
from pyglet.graphics import Batch
import enum
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.gui.events import UIOnClickEvent

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
# или SCREEN_HEIGHT = 900
SCREEN_TITLE = "CupHead"
ANIMATION_SPEED_COIN = 0.1
GRAVITY = 1.1
FIRE_RATE = 0.2
PLAYER_JUMP_SPEED = 25
COLOR = arcade.color.WHITE
CLICK_SOUND = arcade.load_sound('data/others/click.wav')
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


class MenuView(arcade.View):
    def __init__(self, music_sound=None, is_playing=False):
        super().__init__()
        self.background = arcade.load_texture('data/others/background_menu.png')
        self.texture_sound_on = arcade.load_texture('data/others/music_on.png')
        self.texture_sound_off = arcade.load_texture('data/others/music_off.png')
        self.background_music = arcade.load_sound("data/song/Don't Deal With the Devil.mp3")
        self.click_sound = arcade.load_sound('data/others/click.wav')

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
                self.music_button.texture, self.music_button.texture_hovered = self.texture_sound_off, self.texture_sound_off
                self.music_is_playing = True
            else:
                self.background_player.play()
                CLICK_SOUND.play()
                self.music_button.texture, self.music_button.texture_hovered = self.texture_sound_on, self.texture_sound_on
                self.music_is_playing = False

    def start_game(self):
        """Функция запуска игры"""
        game_view = Levels(self.background_player, self.music_button.texture, self.music_is_playing)
        game_view.setup_widgets()
        self.window.show_view(game_view)
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.center_x + 35, self.center_y, self.background.width + 30,
                                                  self.background.height))
        self.manager.draw()


class Levels(arcade.View):
    def __init__(self, music_player, music_texture, is_playing=False):
        super().__init__()
        self.background = arcade.load_texture('data/others/background_menu.png')
        self.background_player = music_player
        self.music_is_playing = is_playing
        self.music_texture = music_texture

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
            arcade.stop_sound(self.background_player)
            CLICK_SOUND.play()
            games_view = MyGame()
            games_view.setup()
            self.window.show_view(games_view)
            self.manager.disable()

        level_2 = UIFlatButton(text="Level 2",
                               width=270,
                               height=55,
                               style=STYLE_BUTTON)
        self.box_layout.add(level_2)

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
            game_view = MenuView(self.background_player, self.music_is_playing)
            self.window.show_view(game_view)
            self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.XYWH(self.center_x + 35, self.center_y, self.background.width + 30,
                                                  self.background.height))
        self.manager.draw()


class PauseView(arcade.View):
    def __init__(self, game_view, background_player):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.background = arcade.load_texture('data/others/pause_menu.png')
        self.background_player = background_player

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
            self.background_player.play()
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
            arcade.stop_sound(self.background_player)
            CLICK_SOUND.play()
            games_view = MyGame()
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
            menu_view = MenuView()
            window.show_view(menu_view)

        self.box_layout.add(exit)

    def on_draw(self):
        self.game_view.on_draw()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(self.center_x, self.center_y, self.background.width,
                                                                   self.background.height))
        self.batch.draw()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            CLICK_SOUND.play()
            self.window.show_view(self.game_view)


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, speed=1300, damage=1, is_vertical=None):
        super().__init__()
        self.texture = arcade.load_texture('data/hero/hero_bullet.png')
        self.change_x = speed
        self.center_x = start_x
        self.center_y = start_y
        self.damage = damage
        self.vertical = is_vertical

        self.player = Hero()

    def update(self, delta_time, bomb_list):
        if (self.center_x >= SCREEN_WIDTH or self.center_x <= 0 or
                self.center_y >= SCREEN_HEIGHT or self.center_y <= 0):
            self.remove_from_sprite_lists()
        is_collisions = arcade.check_for_collision_with_list(self, bomb_list)
        for bomb in is_collisions:
            bomb.remove_from_sprite_lists()
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
        self.hero = Hero()

    def update(self, delta_time) -> None:
        self.center_y -= self.speed * delta_time

        if self.center_y <= 190:
            self.remove_from_sprite_lists()

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.angle += self.rotation_speed * delta_time


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = 0.8
        self.speed = 500
        self.health = 3

        self.idle_texture = arcade.load_texture("data/hero/hero_0.png")
        self.jump_texture = arcade.load_texture('data/hero/hero_3.png')
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(1, 6):
            texture = arcade.load_texture(f'data/hero/hero_{i}.png')
            self.walk_textures.append(texture)

        self.jump_sound = arcade.load_sound("data/hero/jump.mp3")
        self.attack_sound = arcade.load_sound('data/hero/attack.wav')

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.15

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

        self.center_x = 200
        self.center_y = 225

    def update_animation(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.is_shooting:
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

    def update(self, delta_time, keys_pressed, bullet_list, platform_list):
        """ Перемещение персонажа """
        self.dx = 0

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

        if arcade.key.LSHIFT in keys_pressed:
            self.speed = 600
            self.texture_change_delay = 0.1
        else:
            self.texture_change_delay = 0.15
            self.speed = 500

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
                bullet = Bullet(start_x, start_y, is_vertical=True)
                bullet.texture = bullet.texture.rotate_90()
            else:
                if self.face_direction == FaceDirection.RIGHT:
                    start_x = self.center_x + self.width // 3
                    start_y = self.center_y
                    bullet = Bullet(start_x, start_y, is_vertical=False)
                else:
                    start_x = self.center_x - self.width // 3
                    start_y = self.center_y
                    bullet = Bullet(start_x, start_y, -1300, is_vertical=False)
            bullet_list.append(bullet)

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

        self.center_x += self.dx
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

        self.is_walking = self.dx

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
        """ Запуск анимации выстрела """
        self.is_shooting = True
        self.attack_sound.play()
        self.shoot_timer = 0


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)

        self.texture_table = arcade.load_texture('data/others/table.png')
        self.texture_hp = arcade.load_texture('data/HP_table/hp3.png')

        self.texture_background = arcade.load_texture('data/others/background_2.jpeg')

        self.sound_coin = arcade.load_sound("data/coins/voicy_coin.mp3")
        self.background_music = arcade.load_sound('data/others/Die House.mp3')
        self.background_player = None
        self.go_sound = arcade.load_sound('data/song/go_song.mp3')

        self.countdown_active = True
        self.countdown_value = 4
        self.countdown_timer = 0
        self.countdown_interval = 1.0
        self.game_started = False

        self.textures = []
        self.frame = 0
        self.timer = 0
        self.total = 0

    def setup(self):
        self.batch = Batch()
        self.batch_before = Batch()
        self.total_coins = arcade.Text(f'Total coins: {str(self.total)}', SCREEN_WIDTH - 320, 40, COLOR,
                                       25,
                                       font_name='Gill Sans',
                                       batch=self.batch)
        self.player = Hero()
        self.player_list.append(self.player)

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

        self.countdown_active = True
        self.countdown_value = 4
        self.countdown_timer = 0
        self.game_started = False

        self.last_stage = None

        self.timer_bomb = 0.0
        self.timer_bomb_end = 0.0

    def platform_create(self):
        start_x = random.randint(150, 400)
        start_y = random.randint(350, 450)

        # Возможные паттерны изменения высоты
        patterns = [
            [0, 1, -1],  # Вверх, потом вниз
            [0, -1, 1],  # Вниз, потом обратно
        ]

        pattern = random.choice(patterns)

        max_jump_height = 300

        for i in range(3):
            texture_path = 'data/others/platform_1.png'
            platform = arcade.Sprite(texture_path, scale=1.0)

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

                # ПРЕЖДЕ ЧЕМ установить высоту, проверяем доступность
                proposed_y = prev_platform.center_y + (height_change * direction)

                # Проверяем, не слишком ли высоко относительно предыдущей платформы
                if direction == 1:  # Если платформа выше предыдущей
                    # Ограничиваем максимальную разницу высот
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

            # Проверяем доступность с предыдущей платформы (если не первая)
            if i > 0:
                prev_platform = self.platform_list[i - 1]

                # Если текущая платформа выше предыдущей
                if platform.center_y > prev_platform.center_y:
                    height_diff = platform.center_y - prev_platform.center_y
                    # Если разница больше максимальной высоты прыжка, опускаем платформу
                    if height_diff > max_jump_height:
                        platform.center_y = prev_platform.center_y + max_jump_height

            # Проверяем минимальное расстояние по вертикали
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

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture_background,
                                 arcade.rect.XYWH(self.center_x, self.center_y + 150, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.texture_table, arcade.rect.XYWH(self.center_x, 150, 1440, 297))
        self.batch.draw()
        arcade.draw_texture_rect(self.texture_hp, arcade.rect.XYWH(100, SCREEN_HEIGHT - 60, 100, 50))
        self.coin_list.draw()
        self.platform_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.bomb_list.draw()

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
                CLICK_SOUND.play()

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
        if self.countdown_active:
            self.countdown_timer += delta_time

            if self.countdown_timer >= self.countdown_interval:
                self.countdown_timer = 0
                self.countdown_value -= 1

                if self.countdown_value <= 0:
                    self.go_sound.play()
                    self.countdown_active = False
                    self.game_started = True
                    self.background_player = arcade.play_sound(self.background_music, loop=True, volume=0.4)
            return

        if self.game_started:

            self.physics_engine.update()
            self.player_list.update(delta_time, self.keys_pressed, self.bullet_list, self.platform_list)
            self.player_list.update_animation(delta_time)
            self.bullet_list.update(delta_time, self.bomb_list)
            self.bomb_list.update(delta_time)

            for bomb in self.bomb_list:
                bomb.update_animation(delta_time)

            self.update_bomb_time(delta_time)

            self.timer += delta_time
            if self.timer >= ANIMATION_SPEED_COIN:
                self.timer -= ANIMATION_SPEED_COIN
                self.frame = (self.frame + 1) % 12
                self.coin_list[0].texture = self.textures[self.frame]

            is_collision = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for i in is_collision:
                self.total += 1
                self.sound_coin.play()
                self.total_coins = arcade.Text(f'Total coins: {str(self.total)}', SCREEN_WIDTH - 320, 40, COLOR,
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

    def update_bomb_time(self, delta_time):
        """Временный метод для остановки появления бомб"""
        self.timer_bomb += delta_time
        self.timer_bomb_end += delta_time
        if self.timer_bomb >= 0.5:
            if self.timer_bomb_end >= 10:
                return
            self.timer_bomb = 0.0
            bomb = EnemyBomb(random.randint(100, SCREEN_WIDTH - 100), SCREEN_HEIGHT, 300)
            self.bomb_list.append(bomb)

    def on_key_press(self, key, modifiers):
        if not self.game_started:
            return

        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            self.background_player.pause()
            pause_view = PauseView(self, self.background_player)
            self.window.show_view(pause_view)
        if key == arcade.key.SPACE:
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

    def on_key_release(self, key, modifiers):
        if not self.game_started:
            return

        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
menu_view = MenuView()
window.show_view(menu_view)
arcade.run()
