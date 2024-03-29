import random

from A3 import monster
from A3.character import create_character, determine_health_gain
from A3.combat import combat_round, roll_die
from A3.constants import get_monster_chance, get_special_item_chance, get_find_the_stairs_chance, get_max_x, get_max_y,\
    get_min_x, get_min_y, get_extra_commands, get_valid_movement_choices, add_formatting_line
from A3.monster import spawn_monster


def set_exit() -> tuple:
    """
    Set the exit coordinate.

    :postcondition: a random exit coordinate is created
    :postcondition: exit coordinate is against a wall
    :postcondition: exit coordinate is within the boundaries set by get_min_x(), get_max_x(), get_min_y(), get_max_y()
    :return: tuple
    """

    # get the edge axis at random
    wall = random.choice(('x', 'y'))
    # get edge coordinate
    if wall == 'x':
        exit_coordinate = (random.randint(get_min_x(), get_max_x()), random.choice((get_min_y(), get_max_y())))
    else:
        exit_coordinate = (random.choice((get_min_x(), get_max_x())), random.randint(get_min_y(), get_max_y()),)

    return exit_coordinate


def get_movement() -> str:
    """
    Get movement choice from user.

    :postcondition: movement choice obtained
    :return: string
    """

    return input("Which choice do you want to go (n, s, e, w)? Type 'help'... help. Type 'quit' to... quit")


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
        if character['y-coord'] == get_min_y():
            return True
        else:
            return False
    elif direction == 's':
        if character['y-coord'] == get_max_y():
            return True
        else:
            return False
    elif direction == 'e':
        if character['x-coord'] == get_max_x():
            return True
        else:
            return False
    elif direction == 'w':
        if character['x-coord'] == get_min_x():
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


def is_monster_encountered(chance) -> bool:
    """
    Determine if a monster is encountered.

    :param: chance: int
    :precondition: chance is an integer
    :postcondition: whether or not a monster is encountered
    :return: bool
    """

    if chance == 1:
        return True
    else:
        return False


def stab_in_the_back(chance: int) -> int:
    """
    Attempt a stab in the back.

    :param chance: int
    :postcondition: determine how much damage a stab in the back caused
    :return: int
    """

    if chance == 1:
        return roll_die(1, 4)
    else:
        return 0


def equip_special_item(chance: int, the_player: dict):
    """
    Equip the player character with the special item.

    :param chance: int
    :param the_player: dictionary
    :precondition: chance is integer
    :precondition: the_player has structure {'Dexterity': a, 'doctor-note': {'existence': False, 'durability': x}}
    :postcondition: the_player receives a temporary boost to defence

    >>>equip_special_item(1, the_player)
    "You've found a doctor's note! This will certainly come in handy."
    """

    if chance == 1:
        print("You've found a doctor's note! This will certainly come in handy.")
        the_player['doctor-note']['existence'] = True
        the_player['doctor-note']['durability'] = 3
        the_player['Dexterity'] = 99


def weaken_special_item(the_player: dict):
    """
    Lessen the efficacy of the special item.

    :param the_player:
    :param the_player: dictionary
    :precondition: the_player has structure {'doctor-note': {'existence': True, 'durability': 0}}
    :precondition: the_player['doctor-note']['existence'] = True
    :precondition: the_player['doctor-note']['durability'] > 0
    :postcondition: durability of the special item is lessened
    """

    if the_player['doctor-note']['existence']:
        the_player['doctor-note']['durability'] -= 1

        if the_player['doctor-note']['durability'] == 0:
            print("Your doctor's note has disintegrated! Ah well: back to good old hard work")
            the_player['doctor-note']['existence'] = False
            the_player['doctor-note']['durability'] = 0
            the_player['Dexterity'] = 10


def did_user_find_the_stairs(chance: int, the_player: dict):
    """
    Determine if user stumbled upon the stairs.

    :param chance: int
    :param the_player: dictionary
    :precondition: chance is int
    :precondition: the_player has key = 'Floor'
    :precondition: the_player['Floor'] stores an int

    >>> did_user_find_the_stairs(1, the_player{'Floor': 3})
    "Success! You made it to the stairs down!"
    """

    if the_player['Floor'] > 1:
        if chance == 1:
            print("Success! You made it to the stairs down!")
            the_player['Floor'] -= 1
            add_formatting_line()
            print("You're now on floor", the_player['Floor'])


def menacing_glare():
    """
    Spawn a monster to glare menacingly.

    :postcondition: a chilling glare of things to come is presented to the user
    """

    print(monster.generate_monster_name(),
          "wanders by the the newly vacated exit, holding a final exam; peering right at you...")


def did_user_find_exit(floor: int, x_coord: int, y_coord: int, exit_coord: tuple) -> bool:
    """
    Determine if user found the exit.
    
    :param exit_coord: tuple
    :param floor: int
    :param x_coord: int
    :param y_coord: int
    :precondition: exit_coord is size 2
    :precondition: exit_coord elements correspond to (x, y)
    :precondition: exit_coord elements are ints
    :precondition: get_min_x() < exit_coord(0) < get_max_x()
    :precondition: get_min_y() < exit_coord(1) < get_max_y()
    :precondition: floor = 1
    :precondition: get_min_x() < x_coord < get_max_x()
    :precondition: get_min_y() < y_coord < get_max_y()
    :postcondition: determine if the user has magically found the exit
    :return: bool
    """

    if floor == 1:
        # Check to see if x and y match the secretly set-coordinates
        if x_coord == exit_coord[0] and y_coord == exit_coord[1]:
            add_formatting_line()
            add_formatting_line()
            print("You managed to find the exit! Enjoy your time off..... you'll be back")
            menacing_glare()
            add_formatting_line()
            add_formatting_line()
            return True
    else:
        return False


def process_god_mode(movement: str, god_modifiers: dict):
    """
    Process god_mode cheats.

    :param god_modifiers: dictionary
    :param movement: str
    :precondition: god_modifiers has {'items': x, 'stairs': y, escape(a, b)}

    :postcondition: god mode is activated on the chosen game aspect
    """

    if movement == 'god_exit':
        print("The exit is at:", god_modifiers['escape'])
    elif movement == 'god_battle':
        god_modifiers['item'] = apply_god_modification('item', True)
        print("God mode activated: Chance of finding special item increased")
    elif movement == 'god_stairs':
        god_modifiers['stairs'] = apply_god_modification('stairs', True)
        print("God mode activated: Chance of finding stairs increased")


def apply_god_modification(mod_type: str, god: bool) -> int:
    """
    Add a modifier to the special item chance.

    :param mod_type:
    :param mod_type: str
    :param god: int
    :precondition: type in ['stairs', 'item']
    :precondition: god is > 0
    :precondition: god is integer
    :postcondition: provides modifier to increase chance of finding type to 50%
    :return: int

    >>> apply_god_modification('item', True)
    2
    >>> apply_god_modification('item', False)
    0
    >>> apply_god_modification('stairs', True)
    2
    """

    if god:
        # return (get_special_item_chance() - 2) if mod_type == "item" else (get_find_the_stairs_chance() - 5)
        if mod_type == 'item':
            return 13
        elif mod_type == "stairs":
            return 8
    else:
        return 0


def output_help():
    """
    Output help instructions to user.

    :postcondition: Game purpose and help options provided to user

    >>>output_help()
    ****************************************************************************************
            Welcome to ~~Escape from BCIT~~
            A game of daring-do, perilous movements, underwhelming battle and nonsense.

            Your purpose is to find the exit on the 1st floor and escape.
            But beware! Along the way you may encounter instructors whose only goal is to terrorize you
            with learning evaluations!

            Will you escape? Who knows!!!

            Movement commands:
            - n: go north
            - s: go south
            - e: go east
            - w: go west (life is peaceful there.)
            - quit: go back to real life
            - help: print this message

            Context commands:
            These will be explained in their own context.

            God mode:
            - god_battle: increase likelihood of getting battle-determining tech
            - god_stairs: increase likelihood of finding stairs
            - god_exit: the location of the exit

            Note that god-mode cannot be de-activated. I hope your tiny ego can cope.

            Enjoy!
            - Sid Viscous
            ****************************************************************************************
    """

    print("""****************************************************************************************
            Welcome to ~~Escape from BCIT~~
            A game of daring-do, perilous movements, underwhelming battle and nonsense.
            
            Your purpose is to find the exit on the 1st floor and escape.
            But beware! Along the way you may encounter instructors whose only goal is to terrorize you 
            with learning evaluations!
            
            Will you escape? Who knows!!!
            
            Movement commands:
            - n: go north
            - s: go south
            - e: go east
            - w: go west (life is peaceful there.)
            - quit: go back to real life
            - help: print this message
            
            Context commands:
            These will be explained in their own context.
            
            God mode:
            - god_battle: increase likelihood of getting battle-determining tech
            - god_stairs: increase likelihood of finding stairs
            - god_exit: the location of the exit
            
            Note that god-mode cannot be de-activated. I hope your tiny ego can cope.
            
            Enjoy!
            - Sid Viscous
            ****************************************************************************************""")


def play_game():
    """
    Play 'Trapped at BCIT'.

    :postcondition: you are filled with joy and delight
    :postcondition: hours have passed
    """

    player = create_character()
    god_mode = {'stairs': 0, 'item': 0, 'escape': set_exit()}

    print("You find yourself at BCIT DTC on the 6th floor! Try to escape.")

    while player['HP']['Current'] > 0 and not player['Escaped']:
        movement = get_movement()

        if movement.lower() == 'quit':
            print("k bye. But don't think this means you've escaped!")
            break
        elif movement.lower() == "help":
            output_help()

        # Ensure movement is valid
        while not validate_choice(movement, get_valid_movement_choices()) or movement in get_extra_commands():
            if movement in get_extra_commands():
                process_god_mode(movement, god_mode)  # apply changes if god mode was activated
            else:
                advise_of_movement_error(1)

            movement = get_movement()

        # Did you walk into a wall?
        if did_user_hit_a_wall(movement, player):
            advise_of_movement_error(2)
        else:  # Player moves!
            move_char(movement, player)

            if is_monster_encountered(roll_die(1, get_monster_chance())):
                opponent = spawn_monster()

                add_formatting_line()
                print(opponent['Name'], "appears, with a need to evaluate in their eyes! You have no time for this!"
                                        "(Or do you?)")

                fight_or_flight = input("So, what's the deal: fight (choose 'y') or flight (choose 'n')?")
                while not validate_choice(fight_or_flight, ('y', 'n')):
                    fight_or_flight = input("Sorry, you gotta choose to fight ('y') or flee ('n')")

                if fight_or_flight == 'y':
                    while player['HP']['Current'] > 0 and opponent['HP']['Current'] > 0:
                        add_formatting_line()
                        combat_round(player, opponent)
                else:
                    # 10% change you're stabbed, damage 1d4
                    damage_taken = stab_in_the_back(roll_die(1, 10))

                    if damage_taken > 0:
                        print(opponent['Name'], "notices your absence! That cost you", damage_taken, "hp!")
                        player['HP']['Current'] -= damage_taken

                if player['HP']['Current'] > 0:
                    print("You've managed to escape with", player['HP']['Current'], " hp. Let's hope you don't run into"
                                                                                    " another instructor anytime soon.")
                    add_formatting_line()
                    weaken_special_item(player)
                else:
                    print("You have been unable to cope with the workload. See you in PTS.")
            else:
                # Heal (if possible) and output new health
                player['HP']['Current'] += determine_health_gain(player['HP']['Current'], player['HP']['Max'])
                print("Current HP:", player['HP']['Current'])

                # Was the special weapon found?
                equip_special_item(roll_die(1, (get_special_item_chance() - god_mode['item'])), player)

                # Was the stairs down found?
                did_user_find_the_stairs(roll_die(1, get_find_the_stairs_chance() - god_mode['stairs']), player)

                # Did the user find the exit??
                player['Escaped'] = did_user_find_exit(player['Floor'], player['x-coord'], player['y-coord'],
                                                      god_mode['escape'])


def main():
    play_game()


if __name__ == '__main__':
    main()
