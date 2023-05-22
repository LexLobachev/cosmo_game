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
            random.randint(1, y-2),
            random.randint(1, x-2),
            random.randint(1, 20),
            random.choice('+*.:')
        )
        coroutines.append(coroutine)

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


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

