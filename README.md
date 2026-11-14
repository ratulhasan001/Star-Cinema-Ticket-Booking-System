# Star Cinema Ticket Booking System

One of my first Python projects, written in January 2024 while I was learning object-oriented programming. It was my Phitron OOP mid-term exam: a small command-line system for listing cinema shows, viewing a show's seat map and booking seats.

[Problem statement](https://docs.google.com/document/d/1OZH_1S1pcmloJz-PZWwLVbLcx0Zob1YVoWNTvVIXUNI/edit)

## What I practised

- Inheritance: `Hall` extends the `Star_Cinema` base class, which keeps a class-level list of all halls.
- Encapsulation: a hall's shows and seat matrices are private (name-mangled) attributes, reached only through methods.
- Working with a 2D list: each show has its own rows x columns seat matrix.

## Features

- List all shows (ID, movie name, time)
- View the seat map of a show (`.` free, `X` booked) and the number of free seats
- Book one or more seats by row and seat number
- Rejects unknown show IDs, seats outside the hall, seats that are already booked and the same seat chosen twice
- A booking request is all-or-nothing: if any seat is invalid, no seat is booked
- Invalid input re-prompts instead of crashing

The program starts with one 10 x 10 hall and four sample shows.

## Project structure

```
Star-Cinema-Ticket-Booking-System/
├── main.py             # Star_Cinema and Hall classes, input helpers and the menu
└── tests/
    └── test_cinema.py  # unittest tests for booking rules and seat parsing
```

## How to run

Requires Python 3.10 or newer; standard library only.

```bash
git clone https://github.com/ratulhasan001/Star-Cinema-Ticket-Booking-System.git
cd Star-Cinema-Ticket-Booking-System
python3 main.py
```

Menu: `1` view all shows, `2` view available seats, `3` book tickets, `0` exit. When booking, enter each seat as `row seat` using 1-based numbers, for example `3 5` for row 3, seat 5.

## How to test

```bash
python3 -m unittest discover -s tests -v
```

## Sample session

```
Welcome to Star Cinema

1. View all shows
2. View available seats
3. Book tickets
0. Exit
Enter your choice: 1
Shows in hall 1:
  ID   Movie                     Time
  1    The Last of Us            10-01-2024 12:00 PM
  2    Red Dead Redemption       10-01-2024 11:00 PM
  3    Money Heist               10-01-2024 10:00 PM
  4    Peaky Blinders            10-01-2024 9:00 PM
Enter your choice: 3
Enter show ID: 1
Number of tickets (1-100): 2
Enter each seat as: row seat (for example 3 5)
Seat 1: 11 1
Seat (11, 1) does not exist. Rows are 1-10 and seats are 1-10.
Seat 1: 3 5
Seat 2: 4 4
Successfully booked 2 ticket(s): row 3 seat 5, row 4 seat 4.
Enter your choice: 2
Enter show ID: 1
      1  2  3  4  5  6  7  8  9 10
  1   .  .  .  .  .  .  .  .  .  .
  2   .  .  .  .  .  .  .  .  .  .
  3   .  .  .  .  X  .  .  .  .  .
  4   .  .  .  X  .  .  .  .  .  .
  ...
 10   .  .  .  .  .  .  .  .  .  .
98 seats free  (. free, X booked)
Enter your choice: 0
Thank you for visiting Star Cinema. Goodbye!
```

(The menu is reprinted after each action; it is left out here.)

## Later improvements

I revisited this project in 2026 to fix bugs and add tests while keeping the original class design:

- Seat `0` used to map to index `-1` and silently book the last row or seat; seats below 1 are now rejected.
- A booking that failed part-way used to keep the seats booked before the error; booking is now all-or-nothing.
- Invalid input (non-numeric values, unknown show IDs, booked or invalid seats, unknown menu options) used to raise an exception and end the program; it now shows a message and asks again. Ctrl-D or Ctrl-C exits cleanly.
- Adding a show with an existing ID used to wipe that show's bookings; it is now rejected.
- The program now runs from a `main()` function behind `if __name__ == "__main__":`, so the classes can be imported and tested.
- Fixed the movie title typo ("Read Dead Redemption"), made the seat map easier to read, and added type hints, docstrings and unit tests.

## Limitations

- Bookings are kept in memory only and are lost when the program exits.
- The menu works with a single hall, although the classes support several.

---

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
