import tkinter as tk
from core.point import ControlPoint
from core.curve import BezierCurve
from core.utils import create_smooth_control_point

class BezierCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.reset_state()

        # 绑定事件
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Motion>", self.on_motion)

    def reset_state(self):
        """重置画布状态（仅重置绘制状态，不清除已有曲线）"""
        self.points = []  # 当前绘制的点
        self.curves = []  # 所有曲线
        self.current_curve = None
        self.selected_point = None
        self.preview_point = None
        self.drawing_active = False
        self.status_text = "状态: 未开始"  # 统一状态文本

    def start_new_drawing(self):
        """开始新绘制（保留已有曲线）"""
        self.drawing_active = True
        self.points = []  # 只重置当前绘制的点
        self.status_text = "状态: 进行中"
        if hasattr(self.master, 'controls'):
            self.master.controls.update_status()
        self.draw()

    def on_click(self, event):
        """处理鼠标点击事件"""
        if not self.drawing_active:
            # 只处理点选择
            self.select_point(event.x, event.y)
            return

        # 处理新点添加
        self.add_new_point(event.x, event.y)

    def select_point(self, x, y):
        """选择现有控制点"""
        for point in self.points:
            if point.is_clicked(x, y):
                if self.selected_point:
                    self.selected_point.selected = False
                self.selected_point = point
                point.selected = True
                self.draw()
                return

    def add_new_point(self, x, y):
        """添加新控制点"""
        new_point = ControlPoint(x, y)
        self.points.append(new_point)

        if len(self.points) >= 2:
            self.create_curve_segment()

        self.draw()

    def create_curve_segment(self):

        if len(self.points) < 2:
            return

        prev_curve = self.curves[-1] if self.curves else None
        new_point = self.points[-1]
        start_point = self.points[-2]

        # 如果是第一条曲线段或者新曲线，使用简单中点作为控制点
        if prev_curve is None or len(self.points) == 2:
            control_x = (start_point.x + new_point.x) / 2
            control_y = (start_point.y + new_point.y) / 2
        else:
            # 后续曲线段才使用平滑连接
            control_x, control_y = create_smooth_control_point(prev_curve, new_point)

        control_point = ControlPoint(control_x, control_y)
        self.current_curve = BezierCurve(start_point, control_point, new_point)
        self.curves.append(self.current_curve)

    def on_drag(self, event):
        """处理拖拽事件"""
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
        """处理鼠标移动事件"""
        if self.drawing_active and len(self.points) > 0 and not self.selected_point:
            self.preview_point = (event.x, event.y)
            self.draw()

    def on_double_click(self, event):
        """双击结束绘制"""
        if self.drawing_active:
            self.drawing_active = False
            self.selected_point = None
            self.preview_point = None
            self.status_text = "状态: 已完成"
            if hasattr(self.master, 'controls'):
                self.master.controls.update_status()
            self.draw()

    def draw(self):
        """绘制所有元素"""
        self.delete("all")

        # 绘制所有曲线
        for curve in self.curves:
            if len(curve.points) >= 2:
                self.create_line(
                    *[coord for point in curve.points for coord in point],
                    fill="black", width=2
                )

        # 绘制预览线（保持原来的折线形式）
        if self.drawing_active and self.preview_point and len(self.points) > 0:
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
            color = "red" if point == self.selected_point else "silver"
            self.create_oval(
                point.x - point.radius, point.y - point.radius,
                point.x + point.radius, point.y + point.radius,
                fill=color, outline="black"
            )

        # 显示当前状态（与控件保持一致）
        self.create_text(10, 10, text=self.status_text, anchor="nw", fill="black")