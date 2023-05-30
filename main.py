import asyncio
import time
import curses
import random
import os

from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls


TIC_TIMEOUT = 0.1


def draw(canvas):
    rocket_frames = get_rocket_frames()
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)
    canvas_max_y, canvas_max_x = canvas.getmaxyx()

    coroutines = []
    for coroutine in range(100):
        coroutine = blink(
            canvas,
            random.randint(1, canvas_max_y - 2),
            random.randint(1, canvas_max_x - 2),
            random.randint(1, 20),
            random.choice('+*.:')
        )
        coroutines.append(coroutine)

    rocket = animate_spaceship(canvas, canvas_max_y / 2, canvas_max_x / 2, canvas_max_y, canvas_max_x, *rocket_frames)
    coroutines.append(rocket)

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


async def blink(canvas, row, column, blink_timing, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(blink_timing):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(blink_timing):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(blink_timing):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(blink_timing):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def get_rocket_frames():
    folder = 'frames'
    with open(os.path.join(folder, 'rocket_frame_1.txt')) as file:
        rocket_frame_1 = file.read()
    with open(os.path.join(folder, 'rocket_frame_2.txt')) as file:
        rocket_frame_2 = file.read()
    return [rocket_frame_1, rocket_frame_2]


async def animate_spaceship(canvas, row, column, canvas_max_y, canvas_max_x, *frames):
    last_frame = None
    while True:
        for frame in cycle(frames):
            frame_height, frame_width = get_frame_size(frame)
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            rows_direction *= 2
            columns_direction *= 4
            current_row = row + rows_direction
            current_column = column + columns_direction
            if current_row + frame_height > canvas_max_y - 1 or current_row < 2:
                rows_direction = 0
            if current_column + frame_width > canvas_max_x - 1 or current_column < 2:
                columns_direction = 0
            if last_frame:
                draw_frame(canvas, row, column, last_frame, negative=True)

            row += rows_direction
            column += columns_direction

            draw_frame(canvas, row, column, frame)
            last_frame = frame

            for _ in range(2):
                await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

