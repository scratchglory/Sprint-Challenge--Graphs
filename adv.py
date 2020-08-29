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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Create Player
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Get the reverse direction
rev_dir = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"}
# list reverse direction to reverse course
reverse_path = []

# Dict exists
rooms = {}
# from room.py, add the id of the room as an exit
rooms[0] = player.current_room.get_exits()

# While the length of rooms visited is less than the total number of rooms
while len(rooms) < len(room_graph) - 1:
    # If the room hasn't been visited
    if player.current_room.id not in rooms:
        # add the exits for current room to rooms
        rooms[player.current_room.id] = player.current_room.get_exits()
        # grab the last direction traveled in reverse path
        last_dir = reverse_path[-1]
        # take out last exit from exits dict
        rooms[player.current_room.id].remove(last_dir)

    # While there are no rooms to explore.
    while len(rooms[player.current_room.id]) < 1:
        # Pop last direction from reverse_path
        reverse = reverse_path.pop()
        # Append reverse direction to traversal_path
        traversal_path.append(reverse)
        # Next travel in that direction
        player.travel(reverse)

    # Travel to first available exit in the current room
    e_dir = rooms[player.current_room.id].pop(0)
    # Append to the traversal path
    traversal_path.append(e_dir)
    # Append the reverse direction to reverse path
    reverse_path.append(rev_dir[e_dir])
    # Ravel to next room
    player.travel(e_dir)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
