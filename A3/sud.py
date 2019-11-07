from A2 import dungeonsanddragons
from A2.dungeonsanddragons import combat_round
from A3.character import create_character, determine_health_gain
from A3.monster import spawn_monster


def get_max_x():
    """
    Provide constant value for x.

    :postcondition: value for constant x is provided
    :return: int
    """
    return 5


def get_max_y():
    """
        Provide constant value for x.

        :postcondition: value for constant x is provided
        :return: int
        """
    return 5


def create_dungeon():
    """
    Create a X x Y dungeon.

    :postcondition: a single-level dungeon (MAX_X x MAX_Y) is created
    :return: list

    >>>create_dungeon()
    [[[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]], [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]], [[0, 2], [1, 2], [2, 2], [3, 2]
    ,[4, 2]], [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3]], [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4]]]
    """

    game_board = []

    # This works just fine, but it's not as sweet
    for x in range(get_max_x()):
        game_row = [[y, x] for y in range(get_max_y())]

        game_board.append(game_row)

    # The list comprehension works but makes a single list instead of a nested one
    # game_board = [[y, x] for x in range(get_max_x()) for y in range(get_max_y())]

    return game_board


def execute_movement(location, direction):
    """
    Move one space on the board

    :param location: list
    :param direction: int
    :precondition: current_spot is a 2-element list
    :precondition: 0 >= elements in current_spot <= 4
    :precondition: 1 >= choice <= 4
    :postcondition: will generate co-ordinates for where the player moved to
    :return: 2-element list

    >>>execute_movement([1, 2], 1)
    [1, 3]
    >>>execute_movement([1, 5], 1)
    [1, 5]
    >>>execute_movement([1, 2], 3)
    [2, 2]
    """

    new_x = location[0]
    new_y = location[1]

    if direction == 1 and location[1] < get_max_y():  # ie. north
        new_y += 1
    elif direction == 2 and location[1] > 0:  # ie. south
        new_y -= 1
    elif direction == 3 and location[0] < get_max_x():  # ie. east
        new_x += 1
    elif direction == 4 and location[0] > 0:  # ie. west
        new_x -= 1

    return [new_x, new_y]


def get_movement() -> str:
    """
    Get movement choice from user.

    :postcondition: movement choice obtained
    :return: string
    """

    return input("Which choice do you want to go (n, s, e, w)? Type 'quit' to... quit")


def validate_choice(choice: str, valid_choices: tuple) -> bool:
    """
    Validate users movement choice.

    :param valid_choices: tuple
    :param choice: string
    :precondition: valid_choices are strings
    :precondition: valid_choices contains the valid choices to check against
    :return: bool

    >>>validate_choice('n', ('n', 's', 'w', 'e'))
    True
    >>>validate_choice('1', ('n', 's', 'w', 'e'))
    False
    >>>validate_choice('north', ('n', 's', 'w', 'e'))
    False
    >>>validate_choice('g', ('n', 's', 'w', 'e'))
    False
    """

    if choice.lower() in valid_choices:
        return True
    else:
        return False


def advise_of_movement_error(error: int):
    """
    Notify user they made an invalid movement.

    :param error: int
    :precondition: error is 1 if invalid movement option was provided
    :precondition: error is 2 if user hit a wall
    :postcondition: a helpful message is produced

    >>>advise_of_movement_error(1)
    "Invalid movement option. Please enter again (n, s, w, e)"
    >>>advise_of_movement_error(2)
    "You hit a wall; ouch. Try a different choice(n, s, w, e)"
    """

    if error == 1:
        print("Invalid movement option. Please enter again (n, s, w, e)")
    elif error == 2:
        print("You hit a wall; ouch. Try a different choice(n, s, w, e)")


def did_user_hit_a_wall(direction: str, character: dict) -> bool:
    """
    Determine if user hit a wall when moving.

    :param direction: string
    :param character: dictionary
    :precondition: choice is a single character in [n, s, w, e]
    :precondition: character is a dictionary
    :precondition: character contains key "x-coord"
    :precondition: character contains key "y-coord"
    :precondition: -1 > x-coord < 5
    :precondition: -1 > y-coord < 5
    :postcondition: determine whether valid movement choice ran into a wall
    :return: bool

    >>>did_user_hit_a_wall('n', {'x-coord': 0, 'y-coord': 3})
    False
    >>>did_user_hit_a_wall('n', {'x-coord': 0, 'y-coord': 0})
    True
    >>>did_user_hit_a_wall('e', {'x-coord': 4, 'y-coord': 3})
    True
    >>>did_user_hit_a_wall('e', {'x-coord': 0, 'y-coord': 3})
    False
    """

    if direction == 'n':
        if character['y-coord'] == 0:
            return True
        else:
            return False
    elif direction == 's':
        if character['y-coord'] == 4:
            return True
        else:
            return False
    elif direction == 'e':
        if character['x-coord'] == 4:
            return True
        else:
            return False
    elif direction == 'w':
        if character['x-coord'] == 0:
            return True
        else:
            return False


def move_char(direction: str, character: dict):
    """
    Move the character to a new location.

    :param character: dictionary
    :param direction: string
    :precondition: choice is a single character in [n, s, w, e]
    :precondition: character is a dictionary
    :precondition: character contains key "x-coord"
    :precondition: character contains key "y-coord"
    :precondition: -1 > x-coord < 5
    :precondition: -1 > y-coord < 5
    :postcondition: updates character's position

    >>>move_char('s',  {'x-coord': 0, 'y-coord': 0})
    {'x-coord':0, 'y-coord': 1}
    >>>move_char('e', {'x-coord': 0, 'y-coord': 3})
    {'x-coord':1, 'y-coord': 3}
    """

    if direction == 'n':
        character['y-coord'] -= 1
    elif direction == 's':
        character['y-coord'] += 1
    elif direction == 'e':
        character['x-coord'] += 1
    elif direction == 'w':
        character['x-coord'] -= 1


def is_monster_encountered():
    """
    Determine if a monster is encountered.

    :postcondition: whether or not a monster is encountered
    :return: bool
    """

    found = dungeonsanddragons.roll_die(1, 4)

    if found == 1:
        return True
    else:
        return False


def play_game():
    """
    Play 'Trapped at BCIT'.

    :postcondition: you are filled with joy and delight
    :postcondition: hours have passed
    """

    dungeon = create_dungeon()
    player = create_character()

    print("You find yourself at BCIT DTC on the 6th floor! Try to escape.")

    while player['HP']['Current'] > 0:
        movement = get_movement()

        if movement.lower() == 'quit':
            print("k bye. But don't think this means you've escaped!")
            break

        # Ensure movement is valid
        while not validate_choice(movement, ('n', 's', 'w', 'e')):
            advise_of_movement_error(1)
            movement = get_movement()

        # Did you walk into a wall?
        if did_user_hit_a_wall(movement, player):
            advise_of_movement_error(2)
        else:
            move_char(movement, player)

            # Heal (if possible) and output new health
            player['HP']['Current'] += determine_health_gain(player['HP']['Current'], player['HP']['Max'])
            print("Current HP:", player['HP']['Current'])

            if is_monster_encountered():
                monster = spawn_monster()
                print(monster['Name'], "appears, with a need to evaluate in their eyes! You have no time for this!"
                                       "(Or do you?)")

                input("So, what's the deal: fight (choose 1) or flight (choose 2)?")



                while player['HP']['Current'] > 0 and monster['HP']['Current'] > 0:
                    combat_round(player, monster)

                if player['HP']['Current'] > 0:
                    print("You've managed to escape with", player['HP']['Current'], " hp. Let's hope you don't run into"
                                                                                    " another anytime soon.")
                else:
                    print("You have been unable to cope with the workload. Bye")


def main():
    play_game()


if __name__ == '__main__':
    main()
