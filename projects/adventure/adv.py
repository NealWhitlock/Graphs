from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# keep_going = True
# counter = 999999

# while keep_going:
#     if counter % 5000 == 0:
#         print("Counter/Seed at:", counter)
#     counter += 1

# random.seed(counter)


""" THIS SEED VALUE RESULTS IN A PATH 759 STEPS LONG """
random.seed(1224949)


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

# print(player.current_room.id)
# print(traversal_graph)
# print('='*40)

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

    # If there's anything in the unexplored list then assignment move and rev_move
    if unexplored_this_room:
        move = random.choice(unexplored_this_room)
        rev_move = reverse_dict[move]
    """ End of random assignment """


    # Use a stack to push reverse movement commands onto to back out of deadends
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


"""
End My code
"""


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

# In order to run this repeatedly to get a low traversal path 
# I don't want to see any output until done
# if len(traversal_path) < 975:

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

# print("Seed:", counter)
# print("Path:", traversal_path)

    # if len(traversal_path) < 960:
    #     with open('best.py', 'w') as file:
    #         for item in traversal_path:
    #             file.write(item)

    
    #     # 960 beat, so stop
    #     keep_going = False



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
