import arcade

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Tic Tac Toe"

TILE_HEIGHT = 150
TILE_WIDTH = 150

WHITE = arcade.csscolor.WHITE
RED = arcade.csscolor.RED
GREEN = arcade.csscolor.GREEN


class Tile(arcade.SpriteSolidColor):
    def __init__(self, width, height, color, name):
        super().__init__(width, height, color)
        self.name = name


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.set_location(450, 100)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.tile_list = None
        self.tiles_clicked = None
        self.mark_list = None

        self.turn = None

    def setup(self):
        self.tile_list = arcade.SpriteList()
        self.mark_list = arcade.SpriteList()

        self.turn = 0

        for row in range(3):
            for column in range(3):
                tile = Tile(TILE_WIDTH, TILE_HEIGHT, WHITE, (column, row))
                tile.center_x = 100 + 175 * row
                tile.center_y = 100 + 175 * column

                self.tile_list.append(tile)


    def on_draw(self):
        arcade.start_render()
        self.tile_list.draw()
        self.mark_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.tiles_clicked = arcade.get_sprites_at_point((x, y), self.tile_list)

        if len(self.tiles_clicked) > 0:
            print(self.tiles_clicked[0].name)
            if self.turn % 2 == 0:
                mark = arcade.SpriteSolidColor(100, 100, RED)
                mark.center_x = self.tiles_clicked[0].center_x
                mark.center_y = self.tiles_clicked[0].center_y
                self.mark_list.append(mark)
                self.turn += 1
            else:
                mark = arcade.SpriteSolidColor(100, 100, GREEN)
                mark.center_x = self.tiles_clicked[0].center_x
                mark.center_y = self.tiles_clicked[0].center_y
                self.mark_list.append(mark)
                self.turn += 1

    def on_update(self, delta_time: float):
        self.tile_list.update()
        self.mark_list.update()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
