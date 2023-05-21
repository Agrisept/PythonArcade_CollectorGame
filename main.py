"""
Python game
"""
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UP_LIMIT = 1000

SCREEN_TITLE = "(*˘︶˘*).｡.:*♡ Collector ♡*:.｡.(´｡• ᵕ •｡`)"

CHARACTER_SCALING = 0.5
BACKGROUND_SCALING = 1
TILE_SCALING = 0.5
TRINKET_SCALING = 0.5

JUMP_MAX_HEIGHT = 80

PLAYER_MAX_SPEED_X = 4
PLAYER_MAX_SPEED_Y = 5
class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.WHITE)

        self.camera = None
        self.camera_max = 0
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.player_jump = False
        self.jump_start = None

        self.background_list = None
        self.background_sprite = None

        #Better movement
        self.key_right_pressed = False
        self.key_left_pressed = False

        self.collide = False

        self.player_dx = PLAYER_MAX_SPEED_X
        self.player_dy = PLAYER_MAX_SPEED_Y



    def setup(self):

        # Camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Sprite lists
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

        # Use a loop to place some trinkets for our character to pick up
        # Trinket
        """for x in range(128, 1250, 256):
            trinket = arcade.Sprite(":resources:images/items/coinGold.png", TRINKET_SCALING)
            trinket.center_x = x
            trinket.center_y = 96
            self.scene.add_sprite("Trinket", trinket)"""


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

        self.gui_camera.use()
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )



    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = False

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
            if self.player_sprite.center_y >= self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= 2


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()