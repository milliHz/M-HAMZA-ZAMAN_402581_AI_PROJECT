import tkinter as tk
import random
from queue import PriorityQueue
import time

HEIGHT = 650
WIDTH = 1000
INITIAL_AI_SNAKE_COORDS = [(100, 200), (90, 200), (80, 200)]
INITIAL_SNAKE_COORDS = [(100, 100), (90, 100), (80, 100)]
OBSTACLES_COUNT = 20
GAME_TIME = 300 # in seconds


class AISnake:
    def __init__(self, game):
        self.game = game
        self.coordinates = INITIAL_AI_SNAKE_COORDS
        self.direction = "Down"

    def decide_direction(self, food_coords, obstacle_coords, user_snake_coords):
        # A* algorithm for pathfinding
        path = self.greedy_search(food_coords, obstacle_coords, user_snake_coords)
        if path:
            # Move towards the next point in the path
            next_point = path[1]
            head = self.coordinates[0]
            if head[0] < next_point[0]:
                self.direction = "Right"
            elif head[0] > next_point[0]:
                self.direction = "Left"
            elif head[1] < next_point[1]:
                self.direction = "Down"
            else:
                self.direction = "Up"

    def check_collision(self, obstacle_coords):
        x, y = self.coordinates[0]
        def is_collided(obj_coords):
            return obj_coords[0] == x and obj_coords[1] == y
        # Boundary check
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            # Game over condition (you can implement game over logic here)
            self.game.on_ai_snake_died("End! Enemy Snake died because it hit the boundary.")

        # Snake colliding with a obstacle
        for coords in obstacle_coords:
            if is_collided(coords):
                self.game.on_ai_snake_died("End! Enemy Snake died because it hit an obstacle.")

        # Snake colliding with itself
        for body_part in self.coordinates[1:]:
            if is_collided(body_part):
                self.game.on_ai_snake_died("End! Enemy Snake died because it hit itself.")

        for body_part in self.game.snake:
            if is_collided(body_part):
                self.game.on_ai_snake_died("End! Enemy Snake died because it hit User Snake.")

    def move(self):
        head = self.coordinates[0]
        new_head = None
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.coordinates.insert(0, new_head)
        self.coordinates.pop()

    def calculate_direction(self, current, target):
        if current[0] < target[0]:
            return "Right"
        elif current[0] > target[0]:
            return "Left"
        elif current[1] < target[1]:
            return "Down"
        else:
            return "Up"

    def greedy_search(self, food_coords, obstacle_coords, user_snake_coords):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def is_valid(point):
            x, y = point
            return (
                    0 <= x < WIDTH
                    and 0 <= y < HEIGHT
                    and point not in obstacle_coords
                    and point not in user_snake_coords
                    and point not in self.coordinates
            )

        start = self.coordinates[0]
        end = food_coords

        open_set = PriorityQueue()
        open_set.put((heuristic(start, end), (start, self.direction)))
        came_from = {}
        explored = set()

        while not open_set.empty():
            current, direction = open_set.get()[1]
            explored.add(current)
            if current == end:
                path = [current]
                while current in came_from.keys():
                    current = came_from[current]
                    path.append(current)
                return path[::-1]
            moves = {
                "Right": (current[0] + 20, current[1]),
                "Left": (current[0] - 20, current[1]),
                "Up": (current[0], current[1] - 20),
                "Down": (current[0], current[1] + 20),
            }
            if direction == "Right":
                moves.pop("Left")
            elif direction == "Left":
                moves.pop("Right")
            elif direction == "Up":
                moves.pop("Down")
            else:
                moves.pop("Up")
            for move, neighbor in moves.items():
                if is_valid(neighbor):
                    if neighbor not in came_from and neighbor not in explored:
                        priority = heuristic(neighbor, end)
                        open_set.put((priority, (neighbor, move)))
                        came_from[neighbor] = current
                        explored.add(current)
            # for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            #     neighbor = (current[0] + i * 20, current[1] + j * 20)
            #     if is_valid(neighbor):
            #         if neighbor not in came_from and neighbor not in explored:
            #             priority = heuristic(neighbor, end)
            #             open_set.put((priority, neighbor))
            #             came_from[neighbor] = current
            #             explored.add(current)
        return []

    def a_star_pathfinding(self, food_coords, obstacle_coords, user_snake_coords):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def is_valid(point):
            x, y = point
            return (
                    0 <= x < WIDTH
                    and 0 <= y < HEIGHT
                    and point not in obstacle_coords
                    and point not in user_snake_coords
            )

        start = self.coordinates[0]
        end = food_coords

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == end:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + i * 20, current[1] + j * 20)
                tentative_g_score = g_score[current] + 1

                if is_valid(neighbor):
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        priority = tentative_g_score + heuristic(end, neighbor)
                        open_set.put((priority, neighbor))
                        came_from[neighbor] = current
        path = [food_coords]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        if len(path) > 1:
            return path[::-1]
        return []


class SnakeGame:
    def __init__(self, master):
        # Initialising Game Window settings
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("{w}x{h}".format(h=HEIGHT, w=WIDTH))
        self.master.resizable(False, False)

        self.score_label = None
        self.score = 0
        self.ai_score = 0

        self.game_time = GAME_TIME
        self.start_time = time.time()
        self.is_game_over = False
        self.ai_snake_died = False
        self.snake_died = False

        self.canvas = tk.Canvas(self.master, bg="grey", width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.setup_score_board()

        self.snake = INITIAL_SNAKE_COORDS
        self.ai_snake = AISnake(self)
        self.direction = "Right"

        self.obstacles = [self.create_obstacle() for _ in range(OBSTACLES_COUNT)]
        self.food = self.create_food()
        self.master.bind("<KeyPress>", self.change_direction)
        self.update_time()

        self.update()


    def on_snake_died(self, msg: str):
        self.coordinates = [(0, 0)]
        self.snake_died = True
        self.snake = [(0, 0)]
        self.canvas.create_text(
            WIDTH - 80,
            80,
            font=('consolas', 12),
            text="Your Snake Died",
            fill="red",
            tags="Your_snake_died",
        )

    def on_ai_snake_died(self, msg: str):
        self.ai_snake_died = True
        self.ai_snake.coordinates = [(0, 0)]
        self.canvas.create_text(
            WIDTH - 80,
            100,
            font=('consolas', 12),
            text="Enemy Snake Died",
            fill="red",
            tags="enemy_snake_died",
        )

    def max_x(self):
        return (WIDTH // 20) - 1

    def max_y(self):
        return (HEIGHT // 20) - 1

    def setup_score_board(self):
        self.canvas.delete("user_points")
        self.canvas.delete("ai_points")
        self.canvas.create_text(
            WIDTH - 80,
            30,
            font=('consolas', 12),
            text="Score: {}".format(self.score),
            fill="green",
            tags="score",
        )
        self.canvas.create_text(
            WIDTH - 80,
            50,
            font=('consolas', 12),
            text="Enemy Score:   {}".format(self.ai_score),
            fill="green",
            tags="enemy_score",
        )
        # self.score_label = tk.Label(
        #     self.master,
        #     text="Points:{}".format(self.score),
        #     font=('consolas', 20)
        # )
        # self.score_label.pack()
        # self.ai_score_label = tk.Label(
        #     self.master,
        #     text="AI Points:{}".format(self.ai_score),
        #     font=('consolas', 20)
        # )
        # self.ai_score_label.pack()
        pass

    def increase_score(self, of: str):
        if of == 'user':
            self.score += 1
        elif of == 'ai':
            self.ai_score += 1
        self.setup_score_board()

    def create_food(self):
        obstacle_coords = [self.canvas.coords(obstacle) for obstacle in self.obstacles]
        obstacles_x = [coords[0] for coords in obstacle_coords]
        obstacles_y = [coords[1] for coords in obstacle_coords]
        x = random.randint(0, self.max_x()) * 20
        while x in obstacles_x:
            x = random.randint(0, self.max_x()) * 20
        y = random.randint(0, self.max_y()) * 20
        while y in obstacles_y:
            y = random.randint(0, self.max_y()) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="blue", tags="food")
        return food

    def create_obstacle(self):
        x = random.randint(0, 39) * 20
        y = random.randint(0, 29) * 20
        obstacle = self.canvas.create_rectangle(
            x, y, x + 20, y + 20, fill="white"
        )  # Adjust color or appearance as needed
        return obstacle

    def game_over(self, msg):
        self.canvas.delete("all")
        if self.score < self.ai_score:
            won_message = "Enemy Snake Wins!"
        elif self.score > self.ai_score:
            won_message = "Your Snake Wins!"
        else:
            won_message = "Its a draw!"
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            font=('consolas', 20),
            text=msg,
            fill="red",
            tags="gameover",
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 2) + 50,
            font=('consolas', 20),
            text=won_message,
            fill="red",
            tags="gameover",
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            (self.canvas.winfo_height() / 2) + 100,
            font=('consolas', 20),
            text="Your Points: {},  Enemy Points: {}".format(self.score, self.ai_score),
            fill="red",
            tags="gameover",
        )
        self.is_game_over = True

    def is_collided(self, obj, msg):
        obj_coords = self.canvas.coords(obj)  # obj should be the ID of the canvas item
        head_coords = self.snake[0]
        if head_coords[0] == obj_coords[0] and head_coords[1] == obj_coords[1]:
            self.on_snake_died(msg)

    def check_collision(self):
        # Boundary check
        x, y = self.snake[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            # Game over condition (you can implement game over logic here)
            self.on_snake_died("Game Over! Snake hit the boundary.")

        # Snake colliding with a obstacle
        for obstacle in self.obstacles:
            self.is_collided(obstacle, "Game Over! Snake hit an obstacle.")

        # Snake colliding with itself
        for body_part in self.snake[1:]:
            if x == body_part[0] and y == body_part[1]:
                self.on_snake_died("Game Over! Snake hit itself.")

        for body_part in self.ai_snake.coordinates:
            if x == body_part[0] and y == body_part[1]:
                self.on_snake_died("Game Over! Snake hit AI Snake.")
        # message = "Game Over! Snake collided with itself."
        # print(self.snake)
        # for segment in self.snake[1:]:
        #     self.is_collided(segment, message)

    def move_snake(self):
        head = self.snake[0]
        new_head = None
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)
        self.snake.pop()

    def check_for_food(self, head, ai_head):
        def on_food_eaten(by: str):
            print("Food eaten by {}".format(by))
            self.canvas.delete("food")
            self.food = self.create_food()
            self.increase_score(by)

        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))
            on_food_eaten('user')

        if ai_head[0] == food_coords[0] and ai_head[1] == food_coords[1]:
            self.ai_snake.coordinates.append((0, 0))
            on_food_eaten('ai')

    def update_time(self):
        if self.is_game_over:
            return
        if time.time() - self.start_time >= self.game_time:
            self.game_over("Game Over! Time's up!")
        else:
            self.canvas.delete("time")
            self.canvas.create_text(
                80,
                30,
                font=('consolas', 12),
                text="Time: {}".format(int(self.game_time - (time.time() - self.start_time))),
                fill="red",
                tags="time",
            )
            self.master.after(1000, self.update_time)

    def update(self):
        if self.is_game_over:
            return
        self.move_snake()
        self.check_collision()
        head = self.snake[0]
        food_coords = tuple(self.canvas.coords(self.food)[:2])
        obstacle_coords = [tuple(self.canvas.coords(obstacle)[:2]) for obstacle in self.obstacles]
        user_snake_coords = [coords for coords in self.snake]
        self.ai_snake.decide_direction(food_coords, obstacle_coords, user_snake_coords)
        self.ai_snake.move()

        self.canvas.delete("snake")
        if not self.snake_died:
            for segment in self.snake:
                self.canvas.create_rectangle(
                    segment[0],
                    segment[1],
                    segment[0] + 20,
                    segment[1] + 20,
                    fill="green",
                    tags="snake",
                )

        self.canvas.delete("ai_snake")
        if not self.ai_snake_died:
            for segment in self.ai_snake.coordinates:
                self.canvas.create_rectangle(
                    segment[0],
                    segment[1],
                    segment[0] + 20,
                    segment[1] + 20,
                    fill="yellow",
                    tags="ai_snake",
                )

        self.check_for_food(head, self.ai_snake.coordinates[0])
        self.master.after(200, self.update)

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
