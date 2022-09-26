from unittest import TestCase
from unittest.mock import patch

from sand import Pixel, PixelArray, PixelError


class PixelArrayTest(TestCase):
    def setUp(self) -> None:
        self.pixel_array = PixelArray(10, 20)

    def test_set_array(self):
        cols = 10
        rows = 20
        pixels_count = cols * rows
        array = PixelArray.set_array(PixelArray, cols, rows)
        self.assertEqual(pixels_count, len(array))

    def test_get_pixel(self):
        self.pixel_array.array[5, 5] = 1
        self.assertEqual(1, self.pixel_array.get_pixel(5, 5))

    @patch.multiple(Pixel, __abstractmethods__=set())
    def test_move_pixel_to_empty_position(self):
        pixel = Pixel(self.pixel_array, 1, 1, 5)
        self.pixel_array.array[0, 0] = pixel
        self.pixel_array.move(0, 0, 5, 5)
        self.assertEqual(self.pixel_array.array[0, 0], None)
        self.assertEqual(self.pixel_array.array[5, 5], pixel)

    def test_try_move_pixel_to_taken_position(self):
        self.pixel_array.array[0, 0] = 1
        self.pixel_array.array[5, 5] = 1
        with self.assertRaises(PixelError):
            self.pixel_array.move(0, 0, 5, 5)

    def test_try_move_pixel_to_outside_of_array(self):
        self.pixel_array.array[0, 0] = 1
        with self.assertRaises(PixelError):
            self.pixel_array.move(0, 0, 10, 19)

    def test_try_move_pixel_from_outside_to_array(self):
        with self.assertRaises(PixelError):
            self.pixel_array.move(30, 30, 1, 2)


@patch.multiple(Pixel, __abstractmethods__=set())
class PixelTest(TestCase):
    def setUp(self) -> None:
        self.array = PixelArray(10, 20)

    def test_move_pixel(self):
        pixel = Pixel(self.array, 0, 0, 5)
        pixel.move(5, 4)
        self.assertEqual(pixel.x, 5)
        self.assertEqual(pixel.y, 4)
        self.assertEqual(pixel.array.get_pixel(5, 4), pixel)

    def test_try_move_pixel_to_outside_of_array(self):
        pixel = Pixel(self.array, 0, 0, 5)
        with self.assertRaises(PixelError):
            pixel.move(20, 30)
