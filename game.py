import tkinter as tk

class StackerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("เกมต่อบล็อก (Tkinter Built-in)")
        self.WIDTH, self.HEIGHT = 400, 600
        self.BLOCK_HEIGHT, self.INITIAL_WIDTH = 40, 150
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()
        self.root.bind("<space>", self.drop_block)
        self.reset_game()
        self.update_game()

    def reset_game(self):
        self.canvas.delete("all")
        self.block_width = self.INITIAL_WIDTH
        self.block_x, self.block_y = 0, self.HEIGHT - self.BLOCK_HEIGHT * 2
        self.block_speed, self.score, self.game_over = 5, 0, False
        base_x1 = (self.WIDTH - self.INITIAL_WIDTH) // 2
        base_x2 = base_x1 + self.INITIAL_WIDTH
        base_y = self.HEIGHT - self.BLOCK_HEIGHT
        self.stack = [(base_x1, base_x2)]
        self.canvas.create_rectangle(base_x1, base_y, base_x2, base_y + self.BLOCK_HEIGHT, fill="#2980b9", outline="white", tags="stack")
        self.current_block = self.canvas.create_rectangle(self.block_x, self.block_y, self.block_x + self.block_width, self.block_y + self.BLOCK_HEIGHT, fill="#e74c3c", outline="white")
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))

    def update_game(self):
        if not self.game_over:
            self.block_x += self.block_speed
            if self.block_x + self.block_width > self.WIDTH or self.block_x < 0:
                self.block_speed = -self.block_speed
            self.canvas.coords(self.current_block, self.block_x, self.block_y, self.block_x + self.block_width, self.block_y + self.BLOCK_HEIGHT)
            self.root.after(16, self.update_game)

    def drop_block(self, event):
        if self.game_over:
            self.reset_game()
            self.update_game()
            return
        target_x1, target_x2 = self.stack[-1]
        current_x1, current_x2 = self.block_x, self.block_x + self.block_width
        new_x1, new_x2 = max(current_x1, target_x1), min(current_x2, target_x2)
        if new_x1 < new_x2:
            self.block_width = new_x2 - new_x1
            self.block_x = new_x1
            color = "#2ecc71" if len(self.stack) % 2 == 0 else "#3498db"
            self.canvas.create_rectangle(new_x1, self.block_y, new_x2, self.block_y + self.BLOCK_HEIGHT, fill=color, outline="white", tags="stack")
            self.stack.append((new_x1, new_x2))
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.block_speed += 0.7 if self.block_speed > 0 else -0.7
            if self.block_y < self.HEIGHT // 2:
                self.canvas.move("stack", 0, self.BLOCK_HEIGHT)
            else:
                self.block_y -= self.BLOCK_HEIGHT
            self.block_x = 0
        else:
            self.game_over = True
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2, text="GAME OVER", fill="#e74c3c", font=("Arial", 30, "bold"))
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 + 40, text="Press SPACE to Restart", fill="white", font=("Arial", 14))

if __name__ == "__main__":
    root = tk.Tk()
    game = StackerGame(root)
    root.mainloop()