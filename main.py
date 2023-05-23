import asyncio
import time
import curses
import random

TIC_TIMEOUT = 0.1


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    y, x = canvas.getmaxyx()

    coroutines = []
    for coroutine in range(100):
        coroutine = blink(
            canvas,
            random.randint(1, y - 2),
            random.randint(1, x - 2),
            random.randint(1, 20),
            random.choice('+*.:')
        )
        coroutines.append(coroutine)

    fire_shot = fire(canvas, y - 2, x / 2)
    coroutines.append(fire_shot)

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


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

