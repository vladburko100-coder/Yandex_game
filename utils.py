import arcade
from arcade.gui import UIManager

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
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.WHITE,
        bg=(0, 0, 0, 0),
        font_size=43,
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.BROWN,
        bg=(0, 0, 0, 0),
        font_size=43
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_name='Gill Sans',
        font_color=arcade.color.RED_DEVIL,
        bg=(0, 0, 0, 0),
        font_size=43
    )
}


def create_music_log(filename="all_music.txt"):
    """Создание .txt файла со всеми названиями треков в игре"""
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
