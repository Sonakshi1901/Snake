import curses
from curses import KEY_LEFT, KEY_DOWN, KEY_RIGHT, KEY_UP
from random import randint

# setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0)  # lines, columns, ycor, xcor
win.keypad(1)  # want to use keypad
curses.noecho(0)  # don't want to use other input char and echo this to our terminal
curses.curs_set(0)  # hide the cursor
win.border(0)
win.nodelay(1)  # Loop will continue without waiting for user

# Snake and Food
snake = [(4, 10), (4, 9), (4, 8)]  # (y, x)
food = (10, 20)
win.addch(food[0], food[1], '#')

# Game Logic
score = 0
ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, "Score: " + str(score) + ' ')  # (line, column, string)
    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)  # increases speed

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key  # when 'nodelay' is 1

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
        key = prev_key  # will keep moving in right direction

    # Calculate the next coordinates
    y = snake[0][0]  # first tuple and first coordinate of that tuple
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1  # Every time the snake goes down we increase the y coordinate
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1
    snake.insert(0, (y, x))  # inserting a new head in the beginning

    # Check if we hit the border
    if y == 0 or y == 19:  break
    if x == 0 or x == 59:  break

    # If snake runs over itself
    if snake[0] in snake[1:]: break  # snake[0] = head of snake

    if snake[0] == food:
        # eat the food
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))  # random y and x coordinates
            if food in snake:
                food = ()  # this is to make the while loop running
        win.addch(food[0], food[1], '#')
    else:
        # move snake
        last = snake.pop()  # remove the last tuple of the array
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], '*')  # new position of snake

curses.endwin()
print(f"Final score = {score}")
