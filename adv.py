from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

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

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {player.current_room.id: {d: "?" for d in player.current_room.get_exits()}}


def get_unexplored_direction(directions):
    for d in directions:
        if directions[d] == "?":
            return d


def get_path(visited):
    queue, directions = deque(), []
    queue.append([player.current_room.id])

    while len(queue):
        current_path = queue.popleft()
        current_id = current_path[-1]

        for d in graph[current_id]:
            if graph[current_id][d] == "?":
                return [current_path, directions]

        for d in graph[current_id]:
            if graph[current_id][d] not in visited:
                visited.add(player.current_room.id)
                new_path = list(current_path)
                new_path.append(graph[current_id][d])
                queue.append(new_path)
                directions.append(d)
                player.travel(d)
                break


opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}


def generate_traversal_path():
    visited, num_rooms = set(), 1

    while num_rooms < len(world.rooms):
        room_id = player.current_room.id
        random_d = get_unexplored_direction(graph[room_id])

        if random_d:
            traversal_path.append(random_d)
            player.travel(random_d)
            graph[room_id][random_d] = player.current_room.id

            if player.current_room.id not in graph:
                num_rooms += 1
                graph[player.current_room.id] = {
                    d: "?" for d in player.current_room.get_exits()
                }
            graph[player.current_room.id][opposite_directions[random_d]] = room_id
        else:
            res = get_path(visited)

            if res:
                traversal_path.extend(res[1])
            else:
                break


generate_traversal_path()

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
