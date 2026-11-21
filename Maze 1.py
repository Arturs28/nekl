import tkinter as tk
from collections import deque


MAZE = (
    "#########################",
    "#A  #       #           #",
    "# # # ##### # ######### #",
    "# #   #   #   #       # #",
    "# ##### # ##### ##### # #",
    "#     # #     #     #   #",
    "##### # ##### ##### ### #",
    "#   # #     #     #   # #",
    "# # # ##### ##### # # # #",
    "# #       #     #   #   #",
    "# ####### ##### ####### #",
    "#       #     #       # #",
    "# ##### ##### # ##### # #",
    "#     #       #     #  B#",
    "#########################",
)

CELL_SIZE = 26


def find_start_and_goal():
    start = goal = None
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            if cell == "A":
                start = (x, y)
            elif cell == "B":
                goal = (x, y)
    return start, goal


def find_shortest_path(start, goal):
    queue = deque([start])
    parents = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        x, y = current
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            neighbor = (x + dx, y + dy)
            nx, ny = neighbor

            if (
                0 <= ny < len(MAZE)
                and 0 <= nx < len(MAZE[ny])
                and MAZE[ny][nx] != "#"
                and neighbor not in parents
            ):
                parents[neighbor] = current
                queue.append(neighbor)

    if goal not in parents:
        return []

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    return path


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirints")

        width = len(MAZE[0]) * CELL_SIZE
        height = len(MAZE) * CELL_SIZE

        self.status = tk.StringVar(value="Nospiest 'Atrisināt', lai parādītu ceļu")

        tk.Label(root, textvariable=self.status, font=("Segoe UI", 11)).pack(pady=(8, 4))
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white", highlightthickness=1)
        self.canvas.pack(padx=10, pady=5)

        controls = tk.Frame(root)
        controls.pack(pady=(4, 10))
        tk.Button(controls, text="Atrisināt", command=self.solve, width=12).pack(side="left", padx=5)
        tk.Button(controls, text="Atiestatīt", command=self.draw_maze, width=12).pack(side="left", padx=5)

        self.start, self.goal = find_start_and_goal()
        self.animation_id = None
        self.draw_maze()

    def draw_maze(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.canvas.delete("all")
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                left = x * CELL_SIZE
                top = y * CELL_SIZE
                right = left + CELL_SIZE
                bottom = top + CELL_SIZE

                if cell == "#":
                    color = "#263238"
                elif cell == "A":
                    color = "#4CAF50"
                elif cell == "B":
                    color = "#F44336"
                else:
                    color = "#FFFFFF"

                self.canvas.create_rectangle(left, top, right, bottom, fill=color, outline="#CFD8DC")

        self.status.set("Nospiest 'Atrisināt', lai parādītu ceļu")

    def solve(self):
        self.draw_maze()
        path = find_shortest_path(self.start, self.goal)

        if not path:
            self.status.set("Ceļš no A uz B nav atrasts")
            return

        self.status.set(f"Ceļš atrasts — {len(path) - 1} soļi")
        self.animate_path(path, 1)

    def animate_path(self, path, index):
        if index >= len(path):
            return

        x, y = path[index]
        left = x * CELL_SIZE
        top = y * CELL_SIZE
        right = left + CELL_SIZE
        bottom = top + CELL_SIZE

        if (x, y) != self.goal:
            self.canvas.create_rectangle(
                left + 5,
                top + 5,
                right - 5,
                bottom - 5,
                fill="#2196F3",
                outline="#2196F3",
            )

        self.animation_id = self.root.after(35, self.animate_path, path, index + 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()

