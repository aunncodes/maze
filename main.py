import os
import random
import time
import sys
import copy
sys.setrecursionlimit(2147483647) # NOTE: THIS LINE IS RISKY, HOWEVER IF YOU WANT TO DO BIG MAZES IT IS NEEDED
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
bggreen = '\033[42m'
# COLOR REFERENCE
class Maze:
    def __init__(self, w, h):
        self.w = w + (w+1) % 2
        self.h = h + (h+1) % 2
        self.grid = [["█" for _ in range(self.w)] for _ in range(self.h)]
        self.grid[self.h-2][self.w-1] = " "
        self.visited = set()

    def print_maze(self, px, py, color=reset, grid=None):
        gri = grid if grid else self.grid
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                if (x, y) == (px, py):
                    row += red + "■"
                else:
                    row += color + gri[y][x]
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
                    if parent[(x, y)] is not None:
                        x, y = parent[(x, y)]
                    else:
                        break
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
    global wins
    if not cheats: wins += 1
    for i in range(10):
        maze.print_maze(maze.h-1, maze.w-2, green) if i % 2 == 0 else maze.print_maze(maze.h-1, maze.w-2, yellow)
        print("\n\n" + red + "You won! (But you had cheats on so it doesn't count)" if cheats else red + "You won!")
        time.sleep(0.3)
        os.system('cls' if os.name == 'nt' else 'clear')
    print(red + "You won! (But you had cheats on so it doesn't count)" if cheats else "You won!")
    menu()


def main():
    try:
        width = int(input("How long would you like the maze to be? ").strip().lower())
        if 1 >= width:
            raise ValueError
        height = int(input("How tall would you like the maze to be? ").strip().lower())
        if 1 >= height:
            raise ValueError
    except ValueError:
        print("Invalid Input.")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
        return
    global cheats
    cheats = True if input("Would you like to have cheats enabled? Type y or n. ").strip().lower() == 'y' else False
    global maze
    maze = Maze(width, height)
    maze.carve_passages()

    px, py = 1, 1

    gx, gy = maze.w - 1, maze.h - 2
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        maze.print_maze(px, py, green)
        if (px, py) == (gx, gy):
            win()
            return
        inp = input(purple + "Use WASD to move. Type k to see the solution. Press q to quit the maze: " if cheats else "Use WASD to move. Press q to quit the maze: ").lower()
        inp = "" if len(inp) == 0 else inp[-1]
        if inp == 'w' and py > 0 and maze.grid[py - 1][px] == " ":
            py -= 1
        elif inp == 'a' and px > 0 and maze.grid[py][px - 1] == " ":
            px -= 1
        elif inp == 's' and py < maze.h - 1 and maze.grid[py + 1][px] == " ":
            py += 1
        elif inp == 'd' and px < maze.w - 1 and maze.grid[py][px + 1] == " ":
            px += 1
        elif inp == 'q':
            menu()
            return
        elif inp == 'k' and cheats:
            path = maze.solve_bfs((px, py), (gx, gy))
            if path:
                gri = copy.deepcopy(maze.grid.copy())
                for i in range(1, len(path) - 1):
                    x0, y0 = path[i - 1]
                    x1, y1 = path[i]
                    x2, y2 = path[i + 1]
                    if x0 == x1 == x2:
                        gri[y1][x1] = red + "│"
                    elif y0 == y1 == y2:
                        gri[y1][x1] = red + "─"
                    elif (x0 < x1 and y2 > y1) or (y0 > y1 and x2 < x1):
                        gri[y1][x1] = red + "┐"
                    elif (x0 > x1 and y2 > y1) or (y0 > y1 and x2 > x1):
                        gri[y1][x1] = red + "┌"
                    elif (x0 < x1 and y2 < y1) or (y0 < y1 and x2 < x1):
                        gri[y1][x1] = red + "┘"
                    elif (x0 > x1 and y2 < y1) or (y0 < y1 and x2 > x1):
                        gri[y1][x1] = red + "└"
                gri[py][px] = red + "■"
                maze.print_maze(px, py, green, gri)
                input(purple + "Press enter to return to the game >> ")
            else:
                print(red + "No path found.")
                time.sleep(1)


def help():
    print(green + "This is a very simple game. Use w, a, s, and d to move around the maze with your character, and try to solve the maze! W will move you up, A will move you left, S will move you down, D will move you right. If you have cheats enabled, you can press k to view the solution.")
    input(reset + "Press enter to return >> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()
    return

def stats():
    print(green + f"Wins: {wins}")
    input(reset + "Press enter to return >> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()
    return


def menu():
    i = 1
    while True:
        print(black + "=== Main Menu ===")
        print(orange + "1. START" + reset)
        print(orange + "2. HELP" + reset)
        print(orange + "3. STATS" + reset)
        print(orange + "4. QUIT" + reset)
        try:
            inp = int(input(reset + "Enter the number of your choice >> ").lower().strip())
        except ValueError:
            print("Invalid Input.")
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
            return
        os.system('cls' if os.name == 'nt' else 'clear')
        if inp == 1:
            main()
        elif inp == 2:
            help()
        elif inp == 3:
            stats()
        elif inp == 4:
            exit(0)
        i = (i - 1) % 4 + 1

if __name__ == '__main__':
    cheats = False
    wins = 0
    menu()
