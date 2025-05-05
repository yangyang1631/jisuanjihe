import tkinter as tk
from core.point import ControlPoint
from core.curve import BezierCurve
from core.utils import create_smooth_control_point


class BezierCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.points = []
        self.curves = []
        self.current_curve = None
        self.selected_point = None
        self.preview_point = None

        # 绑定事件
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Motion>", self.on_motion)

    def on_click(self, event):
        # 检查是否点击了现有控制点
        for point in self.points:
            if point.is_clicked(event.x, event.y):
                self.selected_point = point
                point.selected = True
                self.draw()
                return

        # 添加新点
        new_point = ControlPoint(event.x, event.y)
        self.points.append(new_point)

        if len(self.points) >= 2:
            # 创建新曲线
            prev_curve = self.curves[-1] if self.curves else None
            if prev_curve is None:
                # 第一条曲线，需要起点和终点
                start_point = self.points[-2]
                end_point = self.points[-1]
                # 控制点取起点和终点的中点
                control_x = (start_point.x + end_point.x) / 2
                control_y = (start_point.y + end_point.y) / 2
                control_point = ControlPoint(control_x, control_y)
            else:
                control_x, control_y = create_smooth_control_point(prev_curve, new_point)
                control_point = ControlPoint(control_x, control_y)

            start_point = self.points[-2]
            self.current_curve = BezierCurve(start_point, control_point, new_point)
            self.curves.append(self.current_curve)

        self.draw()

    def on_drag(self, event):
        if self.selected_point:
            self.selected_point.move_to(event.x, event.y)

            # 只更新相邻曲线
            for i, curve in enumerate(self.curves):
                if curve.start == self.selected_point or curve.end == self.selected_point:
                    if i > 0 and self.curves[i - 1].end == curve.start:
                        # 更新前一条曲线的控制点保持平滑
                        new_ctrl_x, new_ctrl_y = create_smooth_control_point(
                            self.curves[i - 1] if i > 0 else None,
                            curve.end
                        )
                        curve.control.move_to(new_ctrl_x, new_ctrl_y)
                    curve._calculate()

            self.draw()

    def on_motion(self, event):
        if len(self.points) > 0 and not self.selected_point:
            self.preview_point = (event.x, event.y)
            self.draw()

    def on_double_click(self, event):
        self.selected_point = None
        self.draw()

    def draw(self):
        self.delete("all")

        # 绘制曲线
        for curve in self.curves:
            if len(curve.points) >= 2:
                self.create_line(
                    *[coord for point in curve.points for coord in point],
                    fill="black", width=2
                )

        # 绘制预览线
        if self.preview_point and len(self.points) > 0:
            start = self.points[-1]
            control_x = (start.x + self.preview_point[0]) / 2
            control_y = (start.y + self.preview_point[1]) / 2
            self.create_line(
                start.x, start.y,
                control_x, control_y,
                self.preview_point[0], self.preview_point[1],
                fill="gray", dash=(4, 2)
            )

        # 绘制控制点
        for point in self.points:
            color = "red" if point.selected else "silver"
            self.create_oval(
                point.x - point.radius, point.y - point.radius,
                point.x + point.radius, point.y + point.radius,
                fill=color, outline="black"
            )