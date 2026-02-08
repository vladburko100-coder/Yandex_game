import arcade
from game_views import MenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, create_music_log


if __name__ == '__main__':
    create_music_log()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()