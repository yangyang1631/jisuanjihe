import tkinter as tk
from tkinter import ttk

class EditorControls(tk.Frame):
    def __init__(self, master, canvas, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = canvas

        self.start_btn = ttk.Button(
            self,
            text="开始绘制",
            command=self.start_drawing
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)


    def start_drawing(self):
        """开始绘制新曲线"""
        self.canvas.start_new_drawing()
        self.update_status()

    def update_status(self):
        """更新状态显示"""
        status = "进行中" if self.canvas.drawing_active else "已完成"
