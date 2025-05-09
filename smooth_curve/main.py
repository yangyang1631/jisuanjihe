import tkinter as tk
from editor.canvas import BezierCanvas
from editor.controls import EditorControls


class BezierEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("曲线编辑器")

        # 创建控制面板
        self.control_panel = tk.Frame(root)
        self.control_panel.pack(fill=tk.X, padx=5, pady=5)

        # 创建画布
        self.canvas = BezierCanvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 添加控制按钮
        self.controls = EditorControls(
            self.control_panel,
            self.canvas
        )
        self.controls.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = BezierEditor(root)
    root.mainloop()