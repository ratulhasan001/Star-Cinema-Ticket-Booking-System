# Star Cinema (OOP)

A small command-line cinema ticket booking system written in Python as an object-oriented programming exercise (Phitron OOP mid-term exam). A `Star_Cinema` base class keeps a class-level list of halls, and a `Hall` subclass stores its shows and a seat matrix per show using private (name-mangled) attributes. The program starts with one 10 x 10 hall and four sample shows, then runs an interactive booking menu.

[Problem statement](https://docs.google.com/document/d/1OZH_1S1pcmloJz-PZWwLVbLcx0Zob1YVoWNTvVIXUNI/edit)

## Features

- List all shows (ID, movie name, time)
- View the seat map of a show as a grid (`0` = free, `1` = booked)
- Book one or more seats for a show by row and column
- Rejects unknown show IDs, out-of-range seats and seats that are already booked
- Demonstrates inheritance (`Hall` extends `Star_Cinema`) and encapsulation (private attributes accessed through methods)

## Tech stack

- Python 3 (standard library only)

## Project structure

```
star-cinema-oop/
├── main.py     # Star_Cinema and Hall classes, sample data and the menu loop
└── README.md
```

## Getting started

```bash
git clone https://github.com/ratulhasan001/star-cinema-oop.git
cd star-cinema-oop
python3 main.py
```

Menu:

```
1  check all shows
2  view available seats   (asks for a show ID)
3  book tickets           (asks for a show ID and number of tickets)
0  exit
```

When booking, enter each seat on its own line as `row column` using 1-based numbers, for example `3 5` for row 3, seat 5.

## Limitations

- Bookings are kept in memory only and are lost when the program exits.
- Invalid input (unknown show ID, invalid or already-booked seat, unknown menu option) raises an exception, which ends the program instead of re-prompting.
- Seat numbers below 1 are not rejected explicitly.

---

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
