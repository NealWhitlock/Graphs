from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

iteration = 1
target = 960
n_times = 5

while iteration < n_times + 1:

    # Keep going until < 960 reached or I kill the execution
    keep_going = True

    # Counter for iterations and seed (set at -1 since the first thing that happens
    # is to increment it)
    counter = -1

    while keep_going:
        player = Player(world.starting_room)

        # Increment counter and set as random seed
        counter += 1
        # random.seed(count)

        # Print out every 5000 runs just so I can make sure things are happening
        if counter % 10000 == 0:
            print(f"Loop {iteration}/{n_times}; Count:", counter)

        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            To run the whole thing as a loop, indent everything below this
            and make sure to uncomment all the appropriate blocks.
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        """ THIS SEED VALUE RESULTS IN A PATH 959 STEPS LONG """
        # random.seed(1224949)  # Comment this when looping

        

        # Fill this out with directions to walk
        # traversal_path = ['n', 'n']
        traversal_path = []

        """
        ### TODO ###
        # Create algorithm to explore dungeon as efficiently as possible
        """
        # Dictionary to store room exits information
        traversal_graph = {}
        # List to act as a stack for reverse movement commands
        movement_stack = []
        # Track the number of question marks in exits to decide when program done
        question_marks = 0

        # Get current room ID to start
        this_room_id = player.current_room.id
        # Get current room exits
        this_room_exits = player.current_room.get_exits()
        # Start the traversal graph with the first room
        traversal_graph[this_room_id] = {}
        for exit in this_room_exits:
            traversal_graph[this_room_id][exit] = '?'
            question_marks += 1

        # Dictionary to map reversed directions
        reverse_dict = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e'
            }

        """ BEGIN LOOP """

        # Keep going until there are no more question marks
        while True:
            # Start with empty move commands
            move, rev_move = '', ''

            """ This was my original implementation using a structured assignment"""
            """ After iterating through the various permutations for order of cardinal
                directions the lowest I could get to was 991 moves """
            # if 's' in traversal_graph[this_room_id]:
            #     move, rev_move = 's', 'n'
            # elif 'w' in traversal_graph[this_room_id]:
            #     move, rev_move = 'w', 'e'
            # elif 'e' in traversal_graph[this_room_id]:
            #     move, rev_move = 'e', 'w'
            # elif 'n' in traversal_graph[this_room_id]:
            #     move, rev_move = 'n', 's'
            """ End of structured approach"""

            """ Trying a randomized approach to exploring the dungeon """
            # List to store the ? exits
            unexplored_this_room = []

            # Loop through exits to see which haven't been traversed
            for key, val in traversal_graph[this_room_id].items():
                if val == '?':
                    # Save any to list
                    unexplored_this_room.append(key)

            # If there's anything in the unexplored list then assign move and rev_move
            if unexplored_this_room:
                # Pick a move at random and then assign the opposite move
                move = random.choice(unexplored_this_room)
                rev_move = reverse_dict[move]
            """ End of random assignment """

            # Use a stack to push reverse movement commands onto to be able to back out of deadends
            if rev_move:
                movement_stack.append(rev_move)

            # If no unexplored directions in room exits, pop movement command off stack
            if not move:
                move = movement_stack.pop()

            # Save this room's ID
            last_room_id = this_room_id

            # Make movement command and append traversal_path list with movement
            traversal_path.append(move)
            player.travel(move)

            # Get current room's ID and exits
            this_room_id = player.current_room.id
            this_room_exits = player.current_room.get_exits()

            # If current room ID not in traversal graph (adjaceny dictionary) add it with the room exits for the value
            if this_room_id not in traversal_graph:
                traversal_graph[this_room_id] = {}
                for exit in this_room_exits:
                    traversal_graph[this_room_id][exit] = '?'
                    question_marks += 1
            
            # Update previous room's ID dictionary with new room's ID
            if traversal_graph[last_room_id][move] == '?':
                traversal_graph[last_room_id][move] = this_room_id
                question_marks -= 1

            # Update this room's opposite move to point to where we just came from
            if (rev_move != '') and traversal_graph[this_room_id][rev_move] == '?':
                traversal_graph[this_room_id][rev_move] = last_room_id
                question_marks -= 1

            # If everything has been explored
            if question_marks == 0:
                break

        if len(traversal_path) < target:
            keep_going= False

        """
        End of my code (except some condtionals and print statements)
        """

    # TRAVERSAL TEST
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)



    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

    # print("Seed:", counter)
    print("Path:", traversal_path)


    with open('best_paths.py', 'a') as file:
        file.write(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited\n")
        file.write("[")
        for i, item in enumerate(traversal_path):
            if i == (len(traversal_path) - 1):
                file.write(f"'{item}'")
            else:
                file.write(f"'{item}', ")
        file.write("]\n")

    iteration += 1

# if len(traversal_path) < 960:
#     with open('best.py', 'w') as file:
#         for item in traversal_path:
#             file.write(item)





#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
