class ControlPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.selected = False

    def is_clicked(self, mouse_x, mouse_y):
        """检查点是否被点击"""
        dx = self.x - mouse_x
        dy = self.y - mouse_y
        return dx * dx + dy * dy <= self.radius * self.radius

    def move_to(self, x, y):
        """移动点到新位置"""
        self.x = x
        self.y = y