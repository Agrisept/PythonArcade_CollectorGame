"""
Python game
"""
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "(*˘︶˘*).｡.:*♡ Collector ♡*:.｡.(´｡• ᵕ •｡`)"
CHARACTER_SCALING = 0.5
BACKGROUND_SCALING = 1
TILE_SCALING = 0.5
JUMP_MAX_HEIDHT = 80
class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORAL)

        self.camera = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.player_jump = False
        self.jump_start = None
        self.camera_max = 0

    def setup(self):
        # Sprite lists
        self.camera = arcade.Camera(self.width, self.height)
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Background
        image_sours_background = "sprites/Скетч карты.png"
        self.background_sprite = arcade.Sprite(image_sours_background, BACKGROUND_SCALING)
        self.background_sprite.center_x = 700
        self.background_sprite.center_y = 420
        self.background_list.append(self.background_sprite)


        # Player
        image_source = "sprites/Bunny_stand.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 80
        self.player_sprite.center_y = 64

        #Adding in player list for group (To Where -- What)
        self.player_list.append(self.player_sprite)

        # Ground
        for x in range (0, 800, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[290, 160], [512, 96], [256, 96], [324, 96], [768, 96], [200, 830]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            # Wall position
            wall.position = coordinate
            """
            Another way to make wall positions
            wall.center_x = coordinate[0] Maybe wall.center_x = random... without creating 'coordinate_list'
            wall.center_y = coordinate[1] "[0]" - элемент списка, если по-русски
            """
            self.wall_list.append(wall)

    def on_draw(self):
        self.clear()
        # Activate our Camera
        self.background_list.draw()
        self.camera.use()
        self.wall_list.draw()
        self.player_list.draw()



    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.center_y += 30
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.center_x += 30
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.center_x -= 30
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.center_y -= 30

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        # Position the camera
        self.center_camera_to_player()

        if self.player_jump:
            self.player_sprite.center_y += 2 #speed of elevating
            if self.player_sprite.center_y >= self.jump_start + JUMP_MAX_HEIDHT:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= 2



def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()