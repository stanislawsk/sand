from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
PIXEL_SIZE = 5
DRAWING_SPEED = 0.5
SCREEN_TITLE = "Sand"


class PixelError(Exception):
    pass


class PixelList():
    def __init__(self) -> None:
        self.list = []  # type: List[Pixel]

    def append(self, pixel: Pixel):
        self.list.append(pixel)

    def update(self):
        for pixel in self.list:
            pixel.update()

    def draw(self):
        for pixel in self.list:
            pixel.draw()


class PixelArray():
    def __init__(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.array = self.set_array(self.cols, self.rows)

    def set_array(self, cols: int, rows: int):
        array = {}  # type: Dict[tuple, Pixel | None]
        for col in range(cols):
            for row in range(rows):
                array[(col, row)] = None
        return array

    def get_pixel(self, x: int, y: int) -> Pixel | None:
        """ Get pixel for given coordinates."""
        return self.array[(x, y)]

    def move(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        """ Move pixel from start position to end position.

        Args:
            start_x (int): start x position of the pixel
            start_y (int): start y position of the pixel
            end_x (int): end x position of the pixel
            end_y (int): end x position of the pixel
        """
        if end_x >= self.cols or end_x < 0 or end_y >= self.rows or end_y < 0:
            raise PixelError('You cannot move a pixel out of array.')
        elif start_x >= self.cols or start_x < 0 or start_y >= self.rows or start_y < 0:
            raise PixelError('You cannot move a pixel from outside to array.')
        elif self.array[end_x, end_y] is not None:
            raise PixelError('The end position is already taken.')
        else:
            self.array[end_x, end_y] = self.array[start_x, start_y]
            self.array[start_x, start_y] = None


class Pixel(ABC):
    color = arcade.csscolor.GREEN

    def __init__(self, pixel_array: PixelArray, x: int, y: int, size: int = 5) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.array = pixel_array
        self.array.array[(x, y)] = self

    @abstractmethod
    def update(self) -> None:
        """ Movement and pixel logic"""
        pass

    def draw(self) -> None:
        x = self.x * self.size
        y = self.y * self.size
        arcade.draw_lrtb_rectangle_filled(
            left=x,
            right=x + self.size,
            top=y + self.size,
            bottom=y,
            color=self.color
        )

    @property
    def type(self):
        return self.__class__.__name__

    def move(self, new_x: int, new_y: int) -> None:
        """ Move pixel to given coordinate

        Args:
            x (int): destination x coordinate
            y (int): destination y coordinate
        """
        self.array.move(self.x, self.y, new_x, new_y)
        self.x = new_x
        self.y = new_y

    def move_right(self, distance: int = 1) -> None:
        """ Move the pixel to the right by the given distance. """
        self.move(self.x + distance, self.y)

    def move_left(self, distance: int = 1) -> None:
        """ Move the pixel to the left by the given distance. """
        self.move(self.x - distance, self.y)

    def move_down(self, distance: int = 1) -> None:
        """ Move the pixel to the down by the given distance. """
        self.move(self.x, self.y - distance)

    def move_up(self, distance: int = 1) -> None:
        """ Move the pixel to the up by the given distance. """
        self.move(self.x, self.y + distance)

    def is_down(self) -> bool:
        """ Check if there is any other pixel on the bootom of the pixel.

        Returns:
            bool: return true if there is a pixel on the bootom.
        """
        if self.y > 0 and self.array.get_pixel(self.x, self.y - 1) is None:
            return False
        else:
            return True

    def is_up(self) -> bool:
        """ Check if there is any other pixel on the up of the pixel.

        Returns:
            bool: return true if there is a pixel on the up.
        """
        if self.y < self.array.rows - 1 and self.array.get_pixel(self.x, self.y + 1) is None:
            return False
        else:
            return True

    def is_right(self) -> bool:
        """ Check if there is any other pixel on the right of the pixel.

        Returns:
            bool: return true if there is a pixel on the right.
        """
        if self.x < self.array.cols - 1 and self.array.get_pixel(self.x + 1, self.y) is None:
            return False
        else:
            return True

    def is_left(self) -> bool:
        """ Check if there is any other pixel on the left of the pixel.

        Returns:
            bool: return true if there is a pixel on the left.
        """
        if self.x > 0 and self.array.get_pixel(self.x - 1, self.y) is None:
            return False
        else:
            return True

    def is_down_left(self) -> bool:
        """ Check if there is any other pixel on the bootom left corner of the pixel.

        Returns:
            bool: return true if there is a pixel on the bootom left corner.
        """
        if self.y > 0 and self.x > 0 and self.array.get_pixel(self.x - 1, self.y - 1) is None:
            return False
        else:
            return True

    def is_down_right(self) -> bool:
        """ Check if there is any other pixel on the bootom right corner of the pixel.

        Returns:
            bool: return true if there is a pixel on the bootom right corner.
        """
        if self.y > 0 and self.x < self.array.cols - 1 and self.array.get_pixel(self.x + 1, self.y - 1) is None:
            return False
        else:
            return True

    def is_up_left(self) -> bool:
        """ Check if there is any other pixel on the up left corner of the pixel.

        Returns:
            bool: return true if there is a pixel on the up left corner.
        """
        if self.y < self.array.rows - 1 and self.x > 0 and self.array.get_pixel(self.x - 1, self.y + 1) is None:
            return False
        else:
            return True

    def is_up_right(self) -> bool:
        """ Check if there is any other pixel on the up right corner of the pixel.

        Returns:
            bool: return true if there is a pixel on the up right corner.
        """
        if self.y < self.array.rows - 1 and self.x < self.array.cols - 1 and self.array.get_pixel(self.x + 1, self.y + 1) is None:
            return False
        else:
            return True


class SandPixel(Pixel):
    color = arcade.csscolor.YELLOW

    def update(self) -> None:
        if not self.is_down():
            self.move_down()
        elif not self.is_left() and not self.is_down_left():
            self.move_left()
        elif not self.is_right() and not self.is_down_right():
            self.move_right()


class StonePixel(Pixel):
    color = arcade.csscolor.DARK_GREY

    def update(self) -> None:
        pass


PIXEL_LIST = (
    SandPixel,
    StonePixel,
)


def draw_pixel_menu(selected: int, pixels: tuple = PIXEL_LIST,):
    x = 10
    y = SCREEN_HEIGHT - 30
    size = 20
    selected_pixel = pixels[selected]
    for pixel in pixels:
        if pixel is selected_pixel:
            size = 25
        else:
            size = 20
        arcade.draw_lrtb_rectangle_filled(
            left=x,
            right=x + size,
            top=y + size,
            bottom=y,
            color=pixel.color
        )
        y -= size + 10


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.pixel_list = None
        self.pixel_array = None
        self.is_hold_mouse = None
        self.hold_timer = None
        self.selected_pixel = 0

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.is_hold_mouse = False
        self.hold_timer = DRAWING_SPEED
        self.pixel_list = PixelList()

        cols = int(SCREEN_WIDTH / PIXEL_SIZE)
        rows = int(SCREEN_HEIGHT / PIXEL_SIZE)
        self.pixel_array = PixelArray(cols, rows)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button is arcade.MOUSE_BUTTON_LEFT:
            self.is_hold_mouse = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button is arcade.MOUSE_BUTTON_LEFT:
            self.is_hold_mouse = False

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if scroll_y == -1 and self.selected_pixel < len(PIXEL_LIST) - 1:
            self.selected_pixel += 1
        if scroll_y == 1 and self.selected_pixel > 0:
            self.selected_pixel -= 1

    def on_update(self, delta_time: float):
        """Movement and game logic"""
        self.pixel_list.update()
        if self.is_hold_mouse and self.hold_timer > DRAWING_SPEED:
            pixel = PIXEL_LIST[self.selected_pixel](self.pixel_array,
                                                    int(self._mouse_x / PIXEL_SIZE), int(self._mouse_y / PIXEL_SIZE), PIXEL_SIZE)
            self.pixel_list.append(pixel)
            self.hold_timer = 0
        self.hold_timer += 1

    def on_draw(self):
        """Render the screen."""
        self.clear()
        draw_pixel_menu(self.selected_pixel)
        self.pixel_list.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
