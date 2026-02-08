import arcade
from effects import FaceDirection
from utils import FIRE_RATE, GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(arcade.Sprite):
    """Класс снарядом которые выпускает герой"""

    def __init__(self, start_x, start_y, speed=1300, damage=1, is_vertical=None, game_view=None):
        super().__init__()
        self.texture = arcade.load_texture('data/hero/hero_bullet.png')
        self.sound_bomb = arcade.load_sound('data/song/bomb_sound.wav')
        self.change_x = speed
        self.center_x = start_x
        self.center_y = start_y
        self.damage = damage
        self.vertical = is_vertical
        self.game_view = game_view

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
    """Класс бомб из 1 уровня"""

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
        """Обновление анимации вращения"""
        self.angle += self.rotation_speed * delta_time


class EnemyGupi(arcade.Sprite):
    """Класс врага Gupi из 2 уровня """

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

        self.health = 3
        self.scale = 1.7
        self.center_y = 300
        self.center_x = SCREEN_WIDTH - 250

        self.landing = arcade.load_sound('data/enemy/gupi/landing.wav')
        self.jump = arcade.load_sound('data/enemy/gupi/jump.wav')
        self.hit = arcade.load_sound('data/enemy/gupi/hit.wav')
        self.hit1 = arcade.load_sound('data/enemy/gupi/hit1.wav')

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
        """Обновление движения и удара"""
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
    """Класс игрока"""

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

        self.jump_sound = arcade.load_sound("data/hero/jump.wav")
        self.attack_sound = arcade.load_sound('data/hero/fire_sound.wav')
        self.hit_sound = arcade.load_sound('data/song/hit_sound.wav')
        self.dash_sound = arcade.load_sound('data/hero/dash.wav')
        self.death_sound = arcade.load_sound('data/hero/player_death.wav')

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
        """Обновление анимации при ходьбе, прыжке, стрельбе и поражении"""
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
        """Перемещение персонажа и стрельба"""
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
