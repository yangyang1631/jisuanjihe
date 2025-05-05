from .point import ControlPoint


class BezierCurve:
    def __init__(self, start, control, end):
        self.start = start
        self.control = control
        self.end = end
        self.points = []
        self._calculate()

    def _calculate(self):
        """计算贝塞尔曲线上的点"""
        self.points = []
        for t in [i / 100 for i in range(101)]:
            # 二次贝塞尔曲线公式
            x = (1 - t) ** 2 * self.start.x + 2 * (1 - t) * t * self.control.x + t ** 2 * self.end.x
            y = (1 - t) ** 2 * self.start.y + 2 * (1 - t) * t * self.control.y + t ** 2 * self.end.y
            self.points.append((x, y))

    def update_control_point(self, new_x, new_y):
        """更新控制点位置"""
        self.control.move_to(new_x, new_y)
        self._calculate()