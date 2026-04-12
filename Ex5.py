import random

class WumpusWorld:
    def __init__(self, size=4, max_actions=20):
        self.size = size
        self.max_actions = max_actions
        self.actions_taken = 0
        self.agent_alive = True
        self.has_gold = False
        self.wumpus_alive = True
        self.bump = False
        self.scream = False
        self.grid = [["" for _ in range(size)] for _ in range(size)]


        #print(f"Valid indices are 0 to {self.size-1}")
        while True:
            try:
                ar, ac = map(int, input("Enter starting row and col for Agent: ").split())
                if 0 <= ar < size and 0 <= ac < size:
                    self.agent_pos = (ar, ac)
                    break
                else:
                    print("Coordinates out of bounds.")
            except ValueError:
                print("Please enter two integers.")

        print("\n1. Randomly generate world")
        print("2. Manually place entities")
        choice = input("Select option (1/2): ")

        if choice == "1":
            self.place_pits_random()
            self.place_wumpus_random()
            self.place_gold_random()
        else:
            self.place_manual()

    def place_pits_random(self):
        for i in range(self.size):
            for j in range(self.size):

                if (i, j) != self.agent_pos:
                    if random.random() > 0.85:
                        self.grid[i][j] += "P "

    def place_wumpus_random(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)

            if (x, y) != self.agent_pos and "P" not in self.grid[x][y]:
                self.grid[x][y] += "W "
                break

    def place_gold_random(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) != self.agent_pos:
                self.grid[x][y] += "G "
                break

    def place_manual(self):
        num_pits = int(input("Enter number of pits: "))
        for i in range(num_pits):
            while True:
                try:
                    r, c = map(int, input(f"Enter row and col for Pit {i+1}: ").split())
                    self.grid[r][c] += "P "
                    break
                except (IndexError, ValueError):
                    print(f"Error: Invalid coordinates.")


        wr, wc = map(int, input("Enter row and col for Wumpus: ").split())
        self.grid[wr][wc] += "W "
        gr, gc = map(int, input("Enter row and col for Gold: ").split())
        self.grid[gr][gc] += "G "

    def get_possible_moves(self):
        x, y = self.agent_pos
        moves = []
        if x > 0: moves.append("up")
        if x < self.size - 1: moves.append("down")
        if y > 0: moves.append("left")
        if y < self.size - 1: moves.append("right")
        return moves

    def get_sensors(self):
        x, y = self.agent_pos
        smell = breeze = glitter = False
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if "W" in self.grid[nx][ny]: smell = True
                if "P" in self.grid[nx][ny]: breeze = True
        if "G" in self.grid[x][y]: glitter = True
        return smell, breeze, glitter, self.bump, self.scream

    def move(self, direction):
        self.bump = False
        x, y = self.agent_pos
        nx, ny = x, y
        if direction == "up": nx -= 1
        elif direction == "down": nx += 1
        elif direction == "left": ny -= 1
        elif direction == "right": ny += 1

        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.agent_pos = (nx, ny)
        else:
            self.bump = True
        self.check_status()

    def grab(self):
        x, y = self.agent_pos
        if "G" in self.grid[x][y]:
            self.has_gold = True
            self.grid[x][y] = self.grid[x][y].replace("G", "")
            print("Gold grabbed!")

    def check_status(self):
        x, y = self.agent_pos
        if "P" in self.grid[x][y]:
            self.agent_alive = False
            print("Fell into Pit!")
        if "W" in self.grid[x][y]:
            self.agent_alive = False
            print("Killed by Wumpus!")

    def display(self):
        print("\nEnvironment Grid:")
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.agent_pos: print("A ", end="")
                else: print(". ", end="")
            print()
        smell, breeze, glitter, bump, scream = self.get_sensors()
        print(f"\nSensors: Smell={smell}, Breeze={breeze}, Glitter={glitter}, Bump={bump}, Scream={scream}")
        print("Moves:", self.get_possible_moves())
        print("Remaining actions:", self.max_actions - self.actions_taken)

    def play(self):
        while self.agent_alive and self.actions_taken < self.max_actions:
            self.display()
            action = input("Action (up/down/left/right/grab): ").lower()
            if action not in ["up", "down", "left", "right", "grab"]:
                print("Invalid action!")
                continue

            self.actions_taken += 1
            if action in ["up", "down", "left", "right"]: self.move(action)
            elif action == "grab": self.grab()

            if self.has_gold:
                print("\nSUCCESS! You found the Gold!")
                return
        if not self.agent_alive: print("\nGAME OVER: You died.")
        else: print("\nGAME OVER: Out of actions.")


try:
    size = int(input("Enter world size: "))
    max_actions = int(input("Enter max actions: "))
    game = WumpusWorld(size, max_actions)
    game.play()
except ValueError:
    print("Please enter valid numbers for size/actions.")
