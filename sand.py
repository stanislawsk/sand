from __future__ import annotations

from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from typing import ClassVar, Dict, List

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
PIXEL_SIZE = 5
SCREEN_TITLE = "Sand"


class PixelError(Exception):
    pass


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

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = x
        self.y = y
        self.size = size

    @abstractmethod
    def update(self) -> None:
        pass

    def draw(self) -> None:
        arcade.draw_lrtb_rectangle_filled(
            left=self.x,
            right=self.x + self.size,
            top=self.y + self.size,
            bottom=self.y,
            color=self.color
        )

    @property
    def type(self):
        return self.__class__.__name__


# class SandPixel(Pixel):
#     color = arcade.csscolor.YELLOW

#     def update(self) -> None:
#         pass


# class PixelList():
#     def __init__(self) -> None:
#         self.list = []  # type: List[Pixel]

#     def append(self, pixel: Pixel):
#         self.list.append(pixel)

#     def update(self):
#         for pixel in self.list:
#             pixel.update()

#     def draw(self):
#         for pixel in self.list:
#             pixel.draw()


# class MyGame(arcade.Window):
#     """
#     Main application class.
#     """

#     def __init__(self):
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#         arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
#         self.set_viewport(0, 50, 0, 25)

#         self.pixel_list = None

#     def setup(self):
#         """Set up the game here. Call this function to restart the game."""
#         self.pixel_list = PixelList()
#         pixel = SandPixel(10, 10, PIXEL_SIZE)
#         self.pixel_list.append(pixel)

#     def on_update(self, delta_time: float):
#         """Movement and game logic"""
#         self.pixel_list.update()

#     def on_draw(self):
#         """Render the screen."""
#         self.clear()
#         self.pixel_list.draw()


# def main():
#     """Main function"""
#     window = MyGame()
#     window.setup()
#     arcade.run()


# if __name__ == "__main__":
#     main()
