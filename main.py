import asyncio
import time
import curses


TIC_TIMEOUT = 0.1


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    coroutine1 = blink(canvas, 2, 2)
    coroutine2 = blink(canvas, 2, 4)
    coroutine3 = blink(canvas, 2, 6)
    coroutine4 = blink(canvas, 2, 8)
    coroutine5 = blink(canvas, 2, 10)

    coroutines = [coroutine1, coroutine2, coroutine3, coroutine4, coroutine5]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            canvas.refresh()
        time.sleep(TIC_TIMEOUT)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

