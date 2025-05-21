import tkinter as tk
import random

class Star:
    def __init__(self, canvas, x, y, dx, dy, bounciness):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bounciness = bounciness
        self.id = canvas.create_oval(x-5, y-5, x+5, y+5, fill='yellow')

    def move(self):
        self.canvas.move(self.id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= self.canvas.winfo_width():
            self.dx = -self.dx * self.bounciness
        if self.y <= 0 or self.y >= self.canvas.winfo_height():
            self.dy = -self.dy * self.bounciness

class BouncingStarsGame:
    def __init__(self, root, bounciness, obstacle_count, initial_speed_range):
        self.root = root
        self.root.title("Bouncing Stars")
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        self.bounciness = bounciness
        self.obstacle_count = obstacle_count
        self.initial_speed_range = initial_speed_range
        
        self.stars = []
        self.obstacles = []
        self.create_obstacles()
        
        self.root.after(1000, self.create_star)
        self.run_game()

    def create_star(self):
        x = random.randint(50, 750)
        y = 0
        dx = random.uniform(*self.initial_speed_range) * random.choice([-1, 1])
        dy = random.uniform(*self.initial_speed_range)
        star = Star(self.canvas, x, y, dx, dy, self.bounciness)
        self.stars.append(star)
        self.root.after(random.randint(500, 1500), self.create_star)

    def create_obstacles(self):
        for _ in range(self.obstacle_count):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            radius = random.randint(20, 50)
            self.obstacles.append(self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='gray'))

    def run_game(self):
        for star in self.stars:
            star.move()
            self.check_collisions(star)
        self.root.after(20, self.run_game)

    def check_collisions(self, star):
        for obstacle in self.obstacles:
            coords = self.canvas.coords(obstacle)
            if self.check_collision(star, coords):
                star.dx = -star.dx * star.bounciness
                star.dy = -star.dy * star.bounciness

    def check_collision(self, star, coords):
        star_coords = self.canvas.coords(star.id)
        star_x = (star_coords[0] + star_coords[2]) / 2
        star_y = (star_coords[1] + star_coords[3]) / 2
        return (coords[0] < star_x < coords[2]) and (coords[1] < star_y < coords[3])

if __name__ == "__main__":
    root = tk.Tk()
    
    # Randomizing the parameters
    bounciness = random.uniform(0.5, 1.0)  # Between 50% and 100% bounciness
    obstacle_count = random.randint(5, 15)  # Between 5 and 15 obstacles
    initial_speed_range = (1.0, 5.0)  # Initial speed range between 1 and 5
    
    game = BouncingStarsGame(root, bounciness, obstacle_count, initial_speed_range)
    root.mainloop()
