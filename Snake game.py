import tkinter as tk
import tkinter.messagebox as messagebox
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.score = 0
        self.score_label = self.canvas.create_text(20, 10, text="Score: 0", fill="white", anchor="nw")

        self.food = self.create_food()
        self.enemy_snake = None  # Enemy snake object
        self.obstacles = []

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
        return food
    
    def create_enemy_snake(self):
        segments = []
        x = random.randint(0, 17) * 20  # Adjusted to avoid exceeding canvas bounds
        y = random.randint(0, 19) * 20
        for _ in range(3):
            segments.append((x, y))
            x -= 20
        enemy_snake = [self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="blue") for (x, y) in segments]
        return enemy_snake

    def create_obstacle(self, x, y):
        obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="gray")
        self.obstacles.append(obstacle)

    def check_collision(self):
        x, y = self.snake[0]
        if y < 0 or y > 400 or x < 0 or x > 400:
            return True
        return False

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)

    def update(self):
        self.move_snake()
        self.snake = self.snake[:len(self.snake)-1]
        head = self.snake[0]
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        self.canvas.delete("food")
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))
            self.canvas.delete(self.food)
            self.food = self.create_food()
            self.score += 1
            self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

        if self.check_collision() or self.check_collision_with_obstacle():
            messagebox.showinfo("Game Over", "Best luck next time")
            self.game_over()

        for obstacle_coords in self.obstacles:
            if self.check_collision_with_obstacle():
                messagebox.showinfo("Game Over", "Best luck next time")
                self.game_over()

        for segment in self.snake[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                messagebox.showinfo("Game Over", "Best luck next time")
                self.game_over()

        if self.enemy_snake is not None and self.check_collision_with_enemy():
            messagebox.showinfo("Game Over", "Best luck next time")
            self.game_over()

        self.master.after(200, self.update)

    def check_collision_with_enemy(self):
        head = self.snake[0]
        for segment in self.enemy_snake:
            segment_coords = self.canvas.coords(segment)
            if head[0] == segment_coords[0] and head[1] == segment_coords[1]:
                return True
        return False

    def check_collision_with_obstacle(self):
        head = self.snake[0]
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if head[0] == obstacle_coords[0] and head[1] == obstacle_coords[1]:
                return True
        return False

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def game_over(self):
        self.master.destroy()
        messagebox.showinfo("Game Over", "Game Over")
        print('game over')

    def spawn_enemy_snake(self):
        self.enemy_snake = self.create_enemy_snake()
        self.master.after(3000, self.disappear_enemy_snake)

    def disappear_enemy_snake(self):
        for segment in self.enemy_snake:
            self.canvas.delete(segment)
        self.enemy_snake = None
        delay = random.randint(2000, 5000)
        self.master.after(delay, self.spawn_enemy_snake)

    def spawn_obstacle(self):
        obstacle_positions = [(140, 140), (160, 140), (180, 140), (200, 140)]
        for position in obstacle_positions:
            self.create_obstacle(*position)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    game.spawn_enemy_snake()
    game.spawn_obstacle()
    root.mainloop()
