"""Battleship, classic arcade game.

Command :
    mouse click = Place the boat and after Attack the enemy
    r = rotate the boat

Exercises :

1. Change the placement of the grid.
2. Change the number and the size of the boat
"""

from random import randint
from turtle import *

from freegames import line, square

"""Base to create and place the grid on the screen"""
base_player_grid_x = -250
base_player_grid_y = 100
base_enemy_grid_x = 100
base_enemy_grid_y = 100
tiles_size = 25

"""The game status is :
        0 = The game as not started, the player set his boats
        1 = The game is in progress
        2 = The game is finishe
"""
game_status = 0

"""Data to manage the boat (placement, size and position)"""
boat_size = [2, 3, 4]
state = {'boat_vertical_position': True, 'boat_to_set': 0}
state['game_status'] = 0

player_score = {'score': 0}
enemy_score = {'score': 0}

path = Turtle(visible=False)
writer = Turtle(visible=False)

"""All the game will be set on the grid, the data are :
        0 = Neutral information
        1, 2, 3, ... to 9 = This digits will represents the boat
        -1 = The attack failed to touch a boat
        10 = The attack touch a boat
"""
player_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
player_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


enemy_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
enemy_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


def draw_grid(base_x, base_y, size):
    """Draw a grid with a base to start"""
    for i in range(0, 11):
        line(base_x, base_y - i * size, base_x + 10 * size, base_y - i * size)
    for i in range(0, 11):
        line(base_x + i * size, base_y, base_x + i * size, base_y - 10 * size)
    for i in range(0, 10):
        path.penup()
        path.goto(base_x + i * size + 10, base_y + 10)
        path.write(chr(65 + i))
    for i in range(1, 11):
        path.penup()
        path.goto(base_x - 15, base_y - i * size + 10)
        path.write(str(i))


def tap(x, y):
    """Respond to screen tap."""
    if state['game_status'] == 0:
        if inside_grid(x, y, base_player_grid_x, base_player_grid_y):
            add_boat_in_grid(boat_size[state['boat_to_set']], True, x, y)
            draw_square_on_screen_grid(
                base_player_grid_x, base_player_grid_y, player_grid, True
            )
    if state['game_status'] == 1:
        if inside_grid(x, y, base_enemy_grid_x, base_enemy_grid_y):
            update_grid(x, y, False)
            draw_square_on_screen_grid(
                base_enemy_grid_x, base_enemy_grid_y, enemy_grid
            )
            check_end_battle_game()
            enemy_attack()


def inside_grid(x, y, base_x, base_y):
    """Return True if the x,y is within the grid"""
    is_in_base_x = False
    is_in_base_y = False

    if x >= base_x and x <= (base_x + (tiles_size * 10)):
        is_in_base_x = True

    if y <= base_y and y >= (base_y - (tiles_size * 10)):
        is_in_base_y = True

    if is_in_base_y and is_in_base_x:
        return True
    else:
        return False


def draw_square_on_screen_grid(base_x, base_y, grid, drawBoat=False):
    """This section will draw the boat and the attack with a grid"""
    for row in range(0, 10):
        for column in range(0, 10):
            place_x = (int)(base_x + (row * tiles_size)) + 0
            place_y = (int)(base_y - (column * tiles_size)) - 25
            if grid[column][row] == -1:
                square(place_x, place_y, tiles_size, 'black')
            if grid[column][row] > 0 and grid[column][row] < 10 and drawBoat:
                square(place_x, place_y, tiles_size, 'blue')
            if grid[column][row] == 10:
                square(place_x, place_y, tiles_size, 'red')


def update_grid(x, y, playerGrid):
    """This section will update the grid
    This will set 10 if an attack touch or -1 if it failed
    """
    if playerGrid:
        column = y
        row = x
        if player_grid[column][row] > 0:
            player_grid[column][row] = 10
        if player_grid[column][row] == 0:
            player_grid[column][row] = -1
    else:
        column = (int)((y - base_enemy_grid_y) / tiles_size) * -1
        row = (int)((x - base_enemy_grid_x) / tiles_size)
        if enemy_grid[column][row] > 0:
            enemy_grid[column][row] = 10
        if enemy_grid[column][row] == 0:
            enemy_grid[column][row] = -1


def add_boat_in_grid(boat, playerGrid, x=0, y=0):
    """The if both x and y is a -1 the random will be applied"""
    if playerGrid:
        column = (int)((y - base_player_grid_y) / tiles_size) * -1
        row = (int)((x - base_player_grid_x) / tiles_size)
        if state['boat_vertical_position']:
            if check_vertical_grid(row, column, boat, player_grid):
                set_vertical_baot_grid(boat, row, column, playerGrid)
                if find_boat_in_grid(boat, player_grid):
                    set_next_action()
        else:
            if check_horizontal_grid(row, column, boat, player_grid):
                set_horizontal_baot_grid(boat, row, column, playerGrid)
                if find_boat_in_grid(boat, player_grid):
                    set_next_action()
    else:
        is_vertical = randint(0, 10)
        if is_vertical <= 5:
            if check_vertical_grid(x, y, boat, enemy_grid):
                set_vertical_baot_grid(boat, x, y, playerGrid)
            else:
                """This portion will repeat if the enemy didn't find it's place"""
                x = randint(0, 9)
                y = randint(0, 9)
                add_boat_in_grid(boat, playerGrid, x, y)
        else:
            if check_horizontal_grid(x, y, boat, enemy_grid):
                set_horizontal_baot_grid(boat, x, y, playerGrid)
            else:
                """This portion will repeat if the enemy didn't find it's place"""
                x = randint(0, 9)
                y = randint(0, 9)
                add_boat_in_grid(boat, playerGrid, x, y)


def check_vertical_grid(x, y, length, grid):
    """Verfify if there is enough place in vertical"""
    for i in range(0, length):
        if (i + y) >= 10:
            return False
        if grid[y + i][x] != 0:
            return False
    return True


def check_horizontal_grid(x, y, length, grid):
    """Verify if there is enough place in horizontal"""
    for i in range(0, length):
        if (i + x) >= 10:
            return False
        if grid[y][x + i] != 0:
            return False
    return True


def set_vertical_baot_grid(boat, x, y, playerGrid):
    """Set a boat to a vertical way"""
    if playerGrid:
        for i in range(0, boat):
            player_grid[y + i][x] = boat
    else:
        for i in range(0, boat):
            enemy_grid[y + i][x] = boat


def set_horizontal_baot_grid(boat, x, y, playerGrid):
    """Set a boat in a horizontal way"""
    if playerGrid:
        for i in range(0, boat):
            player_grid[y][x + i] = boat
    else:
        for i in range(0, boat):
            enemy_grid[y][x + i] = boat


def change_position():
    """Change the verticality of the boat"""
    if state['boat_vertical_position']:
        state['boat_vertical_position'] = False
    else:
        state['boat_vertical_position'] = True


def set_next_action():
    """This section will change the action in progress
    It will change the boat to set or start the game
    """
    if state['boat_to_set'] < (len(boat_size) - 1):
        state['boat_to_set'] = state['boat_to_set'] + 1
    else:
        state['game_status'] = state['game_status'] + 1


def find_boat_in_grid(boat, grid):
    """Return True if he find at last one part of the boat"""
    for row in range(0, 10):
        for column in range(0, 10):
            if grid[column][row] == boat:
                return True
    return False


def place_the_enemy_boat():
    """Place the enemy boat at a random position in the grid"""
    size = len(boat_size)
    for i in range(0, size):
        new_x = randint(0, 9)
        new_y = randint(0, 9)
        add_boat_in_grid(boat_size[i], False, new_x, new_y)


def enemy_attack():
    """A random attack from the enemy"""
    if state['game_status'] == 1:
        attack_x = randint(0, 9)
        attack_y = randint(0, 9)
        if (
            player_grid[attack_y][attack_x] == -1
            or player_grid[attack_y][attack_x] == 10
        ):
            """Restart the attack is it already attack somewhere"""
            enemy_attack()
        else:
            update_grid(attack_x, attack_y, True)
            draw_square_on_screen_grid(
                base_player_grid_x, base_player_grid_y, player_grid
            )
            check_end_battle_game()


def check_end_battle_game():
    """Check if the Game is finish or not"""
    boat_to_rest = 0
    for i in range(0, len(boat_size)):
        if find_boat_in_grid(boat_size[i], player_grid):
            boat_to_rest += 1
    if boat_to_rest == 0:
        state['game_status'] += 1
        print('player lose')
        return
    else:
        boat_to_rest = 0
        for i in range(0, len(boat_size)):
            if find_boat_in_grid(boat_size[i], enemy_grid):
                boat_to_rest += 1
        if boat_to_rest == 0:
            state['game_status'] += 1
            print('player win')
            return


setup(820, 400, 30, 0)
hideturtle()
tracer(False)
listen()
place_the_enemy_boat()
draw_grid(
    base_player_grid_x, base_player_grid_y, tiles_size
)  # draw the player grid
draw_grid(
    base_enemy_grid_x, base_enemy_grid_y, tiles_size
)    # draw the enemy grid
onkey(lambda: change_position(), 'r')
onscreenclick(tap)
done()