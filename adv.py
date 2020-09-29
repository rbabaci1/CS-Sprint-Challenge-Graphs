from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


came_from = {"n": "s", "s": "n", "e": "w", "w": "e"}


def generate_traversal_path(current_room, directions=None, visited=None):
    # creating a set to hold visited rooms if visited is None
    if visited == None:
        visited = set()
        directions = []

    # finding exits for current_room using player from player and get_exits from room
    for move in player.current_room.get_exits():
        # making moves using travel from player
        player.travel(move)

        # reverse_move if already visited to find new path
        if player.current_room.id in visited:
            player.travel(came_from[move])
        # if its a new room, do the following
        else:
            visited.add(player.current_room.id)
            # adding this move to 'directions'
            directions.append(move)
            # recursive: repeating loop and adding to directions
            generate_traversal_path(player.current_room, directions, visited)
            # go_back to previous room
            player.travel(came_from[move])
            # appending this move to 'directions'
            directions.append(came_from[move])
    return directions


traversal_path = generate_traversal_path(player.current_room)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)


if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# print(f"current room: {player.current_room.get_exits()}")
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
