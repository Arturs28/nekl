import tkinter as tk


CELL_SIZE = 20
ROWS = 30
COLS = 40


class LifeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")

        self.running = False
        self.grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="blue",
        )
        self.canvas.pack(padx=10, pady=10)

        controls = tk.Frame(root)
        controls.pack(pady=(0, 10))

        self.start_button = tk.Button(controls, text="Start", width=10, command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(controls, text="Stop", width=10, command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        tk.Button(controls, text="Clear", width=10, command=self.clear).pack(
            side=tk.LEFT, padx=5
        )

        self.draw_lines()
        self.canvas.bind("<Button-1>", self.draw_cell)
        self.canvas.bind("<B1-Motion>", self.draw_cell)
        self.canvas.bind("<Button-3>", self.erase_cell)
        self.canvas.bind("<B3-Motion>", self.erase_cell)

    def draw_lines(self):
        for row in range(ROWS + 1):
            y = row * CELL_SIZE
            self.canvas.create_line(0, y, COLS * CELL_SIZE, y, fill="#dddddd")
        for col in range(COLS + 1):
            x = col * CELL_SIZE
            self.canvas.create_line(x, 0, x, ROWS * CELL_SIZE, fill="#dddddd")

    def cell_from_event(self, event):
        col = max(0, min(COLS - 1, event.x // CELL_SIZE))
        row = max(0, min(ROWS - 1, event.y // CELL_SIZE))
        return row, col

    def draw_cell(self, event):
        row, col = self.cell_from_event(event)
        self.grid[row][col] = True
        self.redraw()

    def erase_cell(self, event):
        row, col = self.cell_from_event(event)
        self.grid[row][col] = False
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        self.draw_lines()
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col]:
                    x1 = col * CELL_SIZE
                    y1 = row * CELL_SIZE
                    self.canvas.create_rectangle(
                        x1 + 1,
                        y1 + 1,
                        x1 + CELL_SIZE - 1,
                        y1 + CELL_SIZE - 1,
                        fill="black",
                        outline="",
                    )

    def count_neighbors(self, row, col):
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                if 0 <= r < ROWS and 0 <= c < COLS and self.grid[r][c]:
                    count += 1
        return count

    def update(self):
        if not self.running:
            return

        next_grid = [[False for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                neighbors = self.count_neighbors(row, col)
                if self.grid[row][col]:
                    next_grid[row][col] = neighbors in (2, 3)
                else:
                    next_grid[row][col] = neighbors == 3

        self.grid = next_grid
        self.redraw()
        self.root.after(100, self.update)

    def start(self):
        if not self.running:
            self.running = True
            self.update()

    def stop(self):
        self.running = False

    def clear(self):
        self.stop()
        self.grid = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    LifeGame(root)
    root.mainloop()