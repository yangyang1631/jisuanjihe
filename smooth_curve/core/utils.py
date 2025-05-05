def create_smooth_control_point(prev_curve, current_end):
    """创建平滑的控制点（仅用于非第一条曲线）"""
    # 使控制点与前一条曲线的终点对称
    control_x = 2 * prev_curve.end.x - prev_curve.control.x
    control_y = 2 * prev_curve.end.y - prev_curve.control.y
    return control_x, control_y