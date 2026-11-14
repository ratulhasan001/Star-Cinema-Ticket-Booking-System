"""Unit tests for the Star_Cinema and Hall classes."""

import unittest

from main import BOOKED, BookingError, Hall, Star_Cinema, parse_seat


class TestHall(unittest.TestCase):
    def setUp(self) -> None:
        self.hall = Hall(3, 4, 7)
        self.hall.entry_show(1, "Movie A", "10:00 AM")
        self.hall.entry_show(2, "Movie B", "1:00 PM")

    def test_hall_is_registered_with_cinema(self):
        self.assertIsInstance(self.hall, Star_Cinema)
        self.assertIn(self.hall, Star_Cinema.hall_list())

    def test_show_list(self):
        self.assertEqual(self.hall.view_show_list(),
                         [(1, "Movie A", "10:00 AM"), (2, "Movie B", "1:00 PM")])

    def test_duplicate_show_id_rejected(self):
        with self.assertRaises(BookingError):
            self.hall.entry_show(1, "Movie C", "5:00 PM")

    def test_new_show_has_all_seats_free(self):
        self.assertEqual(len(self.hall.available_seats(1)), 12)

    def test_booking_marks_seats(self):
        self.hall.book_seats(1, [(0, 0), (2, 3)])
        free = self.hall.available_seats(1)
        self.assertEqual(len(free), 10)
        self.assertNotIn((0, 0), free)
        self.assertNotIn((2, 3), free)

    def test_shows_have_separate_seat_matrices(self):
        self.hall.book_seats(1, [(1, 1)])
        self.assertIn((1, 1), self.hall.available_seats(2))

    def test_double_booking_rejected(self):
        self.hall.book_seats(1, [(1, 2)])
        with self.assertRaises(BookingError):
            self.hall.book_seats(1, [(1, 2)])

    def test_same_seat_twice_in_one_request_rejected(self):
        with self.assertRaises(BookingError):
            self.hall.book_seats(1, [(0, 1), (0, 1)])
        self.assertEqual(len(self.hall.available_seats(1)), 12)

    def test_invalid_seats_rejected(self):
        for seat in [(3, 0), (0, 4), (-1, 0), (0, -1), (10, 10)]:
            with self.subTest(seat=seat):
                with self.assertRaises(BookingError):
                    self.hall.book_seats(1, [seat])
        self.assertEqual(len(self.hall.available_seats(1)), 12)

    def test_failed_booking_books_nothing(self):
        with self.assertRaises(BookingError):
            self.hall.book_seats(1, [(0, 0), (5, 5)])
        self.assertIn((0, 0), self.hall.available_seats(1))

    def test_unknown_show_rejected(self):
        with self.assertRaises(BookingError):
            self.hall.book_seats(99, [(0, 0)])
        with self.assertRaises(BookingError):
            self.hall.available_seats(99)
        with self.assertRaises(BookingError):
            self.hall.seat_map(99)

    def test_empty_booking_rejected(self):
        with self.assertRaises(BookingError):
            self.hall.book_seats(1, [])

    def test_seat_map_shows_booked_seat(self):
        self.hall.book_seats(1, [(0, 0)])
        lines = self.hall.seat_map(1).splitlines()
        self.assertEqual(len(lines), 1 + 3)  # header + one line per row
        self.assertIn("X", lines[1])
        self.assertNotIn("X", lines[2])

    def test_hall_needs_seats(self):
        with self.assertRaises(ValueError):
            Hall(0, 5, 9)

    def test_matrix_is_private(self):
        self.assertFalse(hasattr(self.hall, "seats"))
        self.assertFalse(hasattr(self.hall, "__seats"))
        self.assertEqual(BOOKED, 1)


class TestParseSeat(unittest.TestCase):
    def test_valid_input_is_converted_to_zero_based(self):
        self.assertEqual(parse_seat("3 5"), (2, 4))
        self.assertEqual(parse_seat(" 1,1 "), (0, 0))

    def test_invalid_input(self):
        for text in ["", "3", "a b", "1 2 3", "1.5 2"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_seat(text)


if __name__ == "__main__":
    unittest.main()
