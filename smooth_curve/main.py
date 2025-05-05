import tkinter as tk
from editor.canvas import BezierCanvas


class BezierEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("贝塞尔曲线编辑器")

        self.canvas = BezierCanvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = BezierEditor(root)
    root.mainloop()