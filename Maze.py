"""
Penguin game using arcade library, with help from the examples at: https://arcade.academy/examples/index.html
"""
import random
import arcade
import os

PLAYER_SCALING = 0.5
COIN_SCALING = 0.25

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect penguins with Different Levels Example"

class FallingPenguin(arcade.Sprite):
    """ Simple sprite that falls down """

    def update(self):
        """ Move the penguins """

        # Fall down
        self.center_y -= 2

        # Did we go off the screen? If so, pop back to the top.
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT

class RisingPenguin(arcade.Sprite):
    """ Simple sprite that falls up """

    def update(self):
        """ Move the penguins """

        # Move up
        self.center_y += 2

        # Did we go off the screen? If so, pop back to the bottom.
        if self.bottom > SCREEN_HEIGHT:
            self.top = 0

class Sounds:
    
    def __init__(self):
        """This class holds all of the sounds that we are going to be using, including sound effects
           and songs for various parts of the game"""
        self.volume = 20
        self.sounds = {"main_1":"IceBlizzard.wav", 
                       "main_2":"IceCream.wav",}
    
    def play_sound(self, sound):
        arcade.Sound(self.sounds[sound]).play(volume=self.volume)

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Background image will be stored in this variable
        self.background = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.follower_list = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.follower_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.level = 1

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BUBBLES)

    def level_1(self):
        for i in range(20):

            # Create the coin instance
            coin = arcade.Sprite("followerPenguin.png", .15)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.follower_list.append(coin)

    def level_2(self):
        for i in range(30):

            # Create the coin instance
            coin = FallingPenguin("followerPenguin.png", .15)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

            # Add the coin to the lists
            self.follower_list.append(coin)

    def level_3(self):
        for i in range(30):

            # Create the coin instance
            coin = RisingPenguin("followerPenguin.png", .15)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(-SCREEN_HEIGHT, 0)

            # Add the coin to the lists
            self.follower_list.append(coin)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        # Image from:
        # http://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html
        self.background = arcade.load_texture("844946240_preview_a78c2a1f4c32a62229751b1e92f6511628c7d610.jpg")

        self.score = 0
        self.level = 1
        
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.follower_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("penguin.png", .25)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(50):

            # Create the coin instance
            coin = arcade.Sprite("followerPenguin.png", COIN_SCALING)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.follower_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # Draw all the sprites.
        self.follower_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLUE, 15)

        output = f"Level: {self.level}"
        arcade.draw_text(output, 10, 35, arcade.color.BLUE, 15)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on the coin sprites (The sprites don't do much in this
        # example though.)
        self.follower_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.follower_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        # See if we should go to level 2
        if len(self.follower_list) == 0 and self.level == 1:
            self.level += 1
            self.level_2()
        # See if we should go to level 3
        elif len(self.follower_list) == 0 and self.level == 2:
            self.level += 1
            self.level_3()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    hand_sound = arcade.load_sound("IceBlizzard.wav")
    arcade.play_sound(hand_sound)
    arcade.run()


if __name__ == "__main__":
    main()
