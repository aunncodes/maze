import os
import random
import time

# COLOR REFERENCE
reset = '\033[0m'
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
orange = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
lightgrey = '\033[37m'
darkgrey = '\033[90m'
lightred = '\033[91m'
lightgreen = '\033[92m'
yellow = '\033[93m'
lightblue = '\033[94m'
pink = '\033[95m'
lightcyan = '\033[96m'
# COLOR REFERENCE

class Maze:
    def __init__(self, w, h):
        self.w = w + 1 if w % 2 == 0 else w
        self.h = h + 1 if h % 2 == 0 else h
        self.grid = [["█" for _ in range(self.w)] for _ in range(self.h)]
        self.grid[self.h - 2][self.w - 2] = " "
        self.visited = set()

    def print_maze(self, px, py, color=reset):
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if (x, y) == (px, py):
                    row += red + "■" + reset
                else:
                    row += color + self.grid[y][x] + reset
            print(row)
        print("\n\n")

    def carve_passages(self, cx=1, cy=1):
        self.grid[cy][cx] = " "
        self.visited.add((cx, cy))

        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)

        for direction in directions:
            if direction == 'N':
                nx, ny = cx, cy - 2
            elif direction == 'S':
                nx, ny = cx, cy + 2
            elif direction == 'E':
                nx, ny = cx + 2, cy
            elif direction == 'W':
                nx, ny = cx - 2, cy

            if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in self.visited:
                if direction == 'N':
                    self.grid[cy - 1][cx] = " "
                elif direction == 'S':
                    self.grid[cy + 1][cx] = " "
                elif direction == 'E':
                    self.grid[cy][cx + 1] = " "
                elif direction == 'W':
                    self.grid[cy][cx - 1] = " "
                self.carve_passages(nx, ny)

    def solve_bfs(self, start, goal):
        queue = [start]
        visited = {start}
        parent = {start: None}
        while queue:
            x, y = queue.pop(0)
            if (x, y) == goal:
                path = []
                while (x, y) is not None:
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.reverse()
                return path
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in visited and self.grid[ny][nx] == " ":
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
        return None

def win():
    for i in range(20):
        maze.print_maze(maze.w - 2, maze.h - 2, green) if i % 2 == 0 else maze.print_maze(maze.w - 2, maze.h - 2, yellow)
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    width, height = 16, 16
    global maze
    maze = Maze(width, height)
    maze.carve_passages()

    px, py = 1, 1
    gx, gy = maze.w - 2, maze.h - 2

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        maze.print_maze(px, py, green)
        if (px, py) == (gx, gy):
            win()
            break
        inp = input(blue + "Use WASD to move: " + reset).lower()
        inp = "" if len(inp) == 0 else inp[-1]
        if inp == 'w' and py > 0 and maze.grid[py - 1][px] == " ":
            py -= 1
        elif inp == 'a' and px > 0 and maze.grid[py][px - 1] == " ":
            px -= 1
        elif inp == 's' and py < maze.h - 1 and maze.grid[py + 1][px] == " ":
            py += 1
        elif inp == 'd' and px < maze.w - 1 and maze.grid[py][px + 1] == " ":
            px += 1

if __name__ == '__main__':
    main()