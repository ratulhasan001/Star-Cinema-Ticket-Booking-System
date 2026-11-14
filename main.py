"""Star Cinema ticket booking system (Phitron OOP mid-term exam project).

``Star_Cinema`` keeps a class-level list of every hall; ``Hall`` extends it
and stores its shows plus one seat matrix per show in private attributes.
Seat positions passed to ``Hall`` methods are 0-based ``(row, col)`` tuples;
the menu works with 1-based numbers and converts them.
"""

from __future__ import annotations

FREE, BOOKED = 0, 1


class BookingError(Exception):
    """Raised for an unknown show, an invalid seat or a seat that is already booked."""


class Star_Cinema:
    """The cinema: keeps a list of all its halls."""

    __hall_list: list[Hall] = []

    def entry_hall(self, hall: Hall) -> None:
        """Register a hall with the cinema."""
        self.__hall_list.append(hall)

    @classmethod
    def hall_list(cls) -> list[Hall]:
        """Return a copy of all registered halls."""
        return list(cls.__hall_list)


class Hall(Star_Cinema):
    """A hall with a fixed seat layout and a list of shows."""

    def __init__(self, rows: int, cols: int, hall_no: int) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("A hall needs at least one row and one column.")
        super().__init__()
        self.__rows = rows
        self.__cols = cols
        self.__hall_no = hall_no
        self.__show_list: list[tuple[int, str, str]] = []
        self.__seats: dict[int, list[list[int]]] = {}
        self.entry_hall(self)

    @property
    def rows(self) -> int:
        return self.__rows

    @property
    def cols(self) -> int:
        return self.__cols

    @property
    def hall_no(self) -> int:
        return self.__hall_no

    def entry_show(self, show_id: int, movie_name: str, time: str) -> None:
        """Add a show and give it an empty seat matrix."""
        if show_id in self.__seats:
            raise BookingError(f"A show with ID {show_id} already exists.")
        self.__show_list.append((show_id, movie_name, time))
        self.__seats[show_id] = [[FREE] * self.__cols for _ in range(self.__rows)]

    def view_show_list(self) -> list[tuple[int, str, str]]:
        """Return all shows as ``(id, movie name, time)`` tuples."""
        return list(self.__show_list)

    def has_show(self, show_id: int) -> bool:
        return show_id in self.__seats

    def __matrix(self, show_id: int) -> list[list[int]]:
        if show_id not in self.__seats:
            raise BookingError(f"Show ID {show_id} does not exist.")
        return self.__seats[show_id]

    def check_seat(self, show_id: int, seat: tuple[int, int]) -> None:
        """Raise ``BookingError`` unless ``seat`` exists and is free for this show."""
        matrix = self.__matrix(show_id)
        row, col = seat
        if not (0 <= row < self.__rows and 0 <= col < self.__cols):
            raise BookingError(
                f"Seat ({row + 1}, {col + 1}) does not exist. "
                f"Rows are 1-{self.__rows} and seats are 1-{self.__cols}.")
        if matrix[row][col] == BOOKED:
            raise BookingError(f"Seat ({row + 1}, {col + 1}) is already booked.")

    def book_seats(self, show_id: int, seats: list[tuple[int, int]]) -> None:
        """Book all ``seats`` for a show, or none of them if any seat is invalid."""
        matrix = self.__matrix(show_id)
        if not seats:
            raise BookingError("No seats were given.")
        if len(set(seats)) != len(seats):
            raise BookingError("The same seat was requested more than once.")
        for seat in seats:
            self.check_seat(show_id, seat)
        for row, col in seats:
            matrix[row][col] = BOOKED

    def available_seats(self, show_id: int) -> list[tuple[int, int]]:
        """Return the free seats of a show as 0-based ``(row, col)`` tuples."""
        matrix = self.__matrix(show_id)
        return [(r, c) for r in range(self.__rows) for c in range(self.__cols)
                if matrix[r][c] == FREE]

    def seat_map(self, show_id: int) -> str:
        """Return the seat matrix as text: ``.`` is free, ``X`` is booked."""
        matrix = self.__matrix(show_id)
        header = "     " + " ".join(f"{c:>2}" for c in range(1, self.__cols + 1))
        lines = [header]
        for r, row in enumerate(matrix, start=1):
            cells = " ".join(" X" if seat == BOOKED else " ." for seat in row)
            lines.append(f"{r:>3}  {cells}")
        return "\n".join(lines)

    def view_available_seats(self, show_id: int) -> None:
        """Print the seat map of a show."""
        print(self.seat_map(show_id))


# ---------------------------------------------------------------- user input
def parse_seat(text: str) -> tuple[int, int]:
    """Turn user input like ``"3 5"`` (1-based row and seat) into ``(2, 4)``."""
    parts = text.replace(",", " ").split()
    if len(parts) != 2 or not all(p.lstrip("-").isdigit() for p in parts):
        raise ValueError("Enter the row and seat number separated by a space, e.g. 3 5.")
    row, col = int(parts[0]), int(parts[1])
    return row - 1, col - 1


def ask_int(prompt: str, minimum: int | None = None, maximum: int | None = None) -> int:
    """Keep asking until the user enters a whole number in [minimum, maximum]."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter a number of at least {minimum}.")
        elif maximum is not None and value > maximum:
            print(f"Please enter a number no greater than {maximum}.")
        else:
            return value


def ask_show_id(hall: Hall) -> int:
    while True:
        show_id = ask_int("Enter show ID: ")
        if hall.has_show(show_id):
            return show_id
        print(f"Show ID {show_id} does not exist. Choose 1 to see all shows.")


def show_all(hall: Hall) -> None:
    print(f"Shows in hall {hall.hall_no}:")
    print(f"  {'ID':<4} {'Movie':<25} Time")
    for show_id, movie, time in hall.view_show_list():
        print(f"  {show_id:<4} {movie:<25} {time}")


def book_tickets(hall: Hall) -> None:
    show_id = ask_show_id(hall)
    free = len(hall.available_seats(show_id))
    if free == 0:
        print("Sorry, this show is sold out.")
        return
    count = ask_int(f"Number of tickets (1-{free}): ", 1, free)
    print("Enter each seat as: row seat (for example 3 5)")
    seats: list[tuple[int, int]] = []
    while len(seats) < count:
        try:
            seat = parse_seat(input(f"Seat {len(seats) + 1}: "))
            hall.check_seat(show_id, seat)
        except (ValueError, BookingError) as error:
            print(error)
            continue
        if seat in seats:
            print("You have already chosen that seat.")
            continue
        seats.append(seat)
    hall.book_seats(show_id, seats)
    booked = ", ".join(f"row {r + 1} seat {c + 1}" for r, c in seats)
    print(f"Successfully booked {count} ticket(s): {booked}.")


def main() -> None:
    hall = Hall(10, 10, 1)
    hall.entry_show(1, "The Last of Us", "10-01-2024 12:00 PM")
    hall.entry_show(2, "Red Dead Redemption", "10-01-2024 11:00 PM")
    hall.entry_show(3, "Money Heist", "10-01-2024 10:00 PM")
    hall.entry_show(4, "Peaky Blinders", "10-01-2024 9:00 PM")

    print("Welcome to Star Cinema")
    try:
        while True:
            print("\n1. View all shows")
            print("2. View available seats")
            print("3. Book tickets")
            print("0. Exit")
            choice = ask_int("Enter your choice: ")
            if choice == 1:
                show_all(hall)
            elif choice == 2:
                show_id = ask_show_id(hall)
                hall.view_available_seats(show_id)
                print(f"{len(hall.available_seats(show_id))} seats free  (. free, X booked)")
            elif choice == 3:
                book_tickets(hall)
            elif choice == 0:
                break
            else:
                print("Invalid choice. Please enter 0, 1, 2 or 3.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Thank you for visiting Star Cinema. Goodbye!")


if __name__ == "__main__":
    main()
