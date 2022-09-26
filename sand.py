from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Dict, List

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
PIXEL_SIZE = 5
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
        pass

    def move(self, new_x: int, new_y: int):
        """ Move pixel to given coordinate

        Args:
            x (int): destination x coordinate
            y (int): destination y coordinate
        """
        self.array.move(self.x, self.y, new_x, new_y)
        self.x = new_x
        self.y = new_y

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


class SandPixel(Pixel):
    color = arcade.csscolor.YELLOW

    def update(self) -> None:
        self.move(self.x, self.y - 1)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.set_viewport(0, 50, 0, 25)

        self.pixel_list = None
        self.pixel_array = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.pixel_list = PixelList()
        cols = int(SCREEN_WIDTH / PIXEL_SIZE)
        rows = int(SCREEN_HEIGHT / PIXEL_SIZE)
        self.pixel_array = PixelArray(cols, rows)
        pixel = SandPixel(self.pixel_array, 30, 50, PIXEL_SIZE)
        self.pixel_list.append(pixel)

    def on_update(self, delta_time: float):
        """Movement and game logic"""
        self.pixel_list.update()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.pixel_list.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
