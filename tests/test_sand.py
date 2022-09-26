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
        pixel = Pixel(self.pixel_array, 1, 1)
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
        pixel = Pixel(self.array, 0, 0)
        pixel.move(5, 4)
        self.assertEqual(pixel.x, 5)
        self.assertEqual(pixel.y, 4)
        self.assertEqual(pixel.array.get_pixel(5, 4), pixel)

    def test_try_move_pixel_to_outside_of_array(self):
        pixel = Pixel(self.array, 0, 0)
        with self.assertRaises(PixelError):
            pixel.move(20, 30)

    def test_move_right(self):
        pixel = Pixel(self.array, 0, 0)
        pixel.move_right(2)
        self.assertEqual(pixel.x, 2)

    def test_move_left(self):
        pixel = Pixel(self.array, 5, 0)
        pixel.move_left(2)
        self.assertEqual(pixel.x, 3)

    def test_move_down(self):
        pixel = Pixel(self.array, 0, 5)
        pixel.move_down(2)
        self.assertEqual(pixel.y, 3)

    def test_move_up(self):
        pixel = Pixel(self.array, 0, 0)
        pixel.move_up(2)
        self.assertEqual(pixel.y, 2)

    def test_is_down(self):
        pixel_1 = Pixel(self.array, 0, 1)
        pixel_2 = Pixel(self.array, 0, 0)
        self.assertTrue(pixel_1.is_down())
        self.assertTrue(pixel_2.is_down())

    def test_is_not_down(self):
        pixel = Pixel(self.array, 0, 1)
        self.assertFalse(pixel.is_down())

    def test_is_up(self):
        pixel_1 = Pixel(self.array, 0, 18)
        pixel_2 = Pixel(self.array, 0, 19)
        self.assertTrue(pixel_1.is_up())
        self.assertTrue(pixel_2.is_up())

    def test_is_not_up(self):
        pixel = Pixel(self.array, 0, 1)
        self.assertFalse(pixel.is_up())

    def test_is_right(self):
        pixel_1 = Pixel(self.array, 8, 0)
        pixel_2 = Pixel(self.array, 9, 0)
        self.assertTrue(pixel_1.is_right())
        self.assertTrue(pixel_2.is_right())

    def test_is_not_right(self):
        pixel = Pixel(self.array, 0, 0)
        self.assertFalse(pixel.is_right())

    def test_is_left(self):
        pixel_1 = Pixel(self.array, 1, 0)
        pixel_2 = Pixel(self.array, 0, 0)
        self.assertTrue(pixel_1.is_left())
        self.assertTrue(pixel_2.is_left())

    def test_is_not_left(self):
        pixel = Pixel(self.array, 1, 0)
        self.assertFalse(pixel.is_left())

    def test_is_down_left(self):
        pixel_1 = Pixel(self.array, 1, 2)
        pixel_2 = Pixel(self.array, 0, 1)
        self.assertTrue(pixel_1.is_down_left())
        self.assertTrue(pixel_2.is_down_left())

    def test_is_not_down_left(self):
        pixel = Pixel(self.array, 1, 1)
        self.assertFalse(pixel.is_down_left())

    def test_is_down_right(self):
        pixel_1 = Pixel(self.array, 8, 2)
        pixel_2 = Pixel(self.array, 9, 1)
        self.assertTrue(pixel_1.is_down_right())
        self.assertTrue(pixel_2.is_down_right())

    def test_is_not_down_right(self):
        pixel = Pixel(self.array, 1, 1)
        self.assertFalse(pixel.is_down_right())

    def test_is_up_right(self):
        pixel_1 = Pixel(self.array, 8, 18)
        pixel_2 = Pixel(self.array, 9, 19)
        self.assertTrue(pixel_1.is_up_right())
        self.assertTrue(pixel_2.is_up_right())

    def test_is_not_up_right(self):
        pixel = Pixel(self.array, 1, 1)
        self.assertFalse(pixel.is_up_right())

    def test_is_up_left(self):
        pixel_1 = Pixel(self.array, 1, 18)
        pixel_2 = Pixel(self.array, 0, 19)
        self.assertTrue(pixel_1.is_up_left())
        self.assertTrue(pixel_2.is_up_left())

    def test_is_not_up_left(self):
        pixel = Pixel(self.array, 1, 1)
        self.assertFalse(pixel.is_up_left())
