from core.constants import cfg, WX_MIN, WX_MAX, WY_MIN, WY_MAX


def screen_to_world(sx: int, sy: int) -> tuple[float, float]:
    VP_W  = cfg["VP_W"]
    WIN_H = cfg["WIN_H"]
    VP_H  = cfg["VP_H"]

    fx = sx / VP_W
    fy = (WIN_H - sy) / VP_H
    wx = WX_MIN + fx * (WX_MAX - WX_MIN)
    wy = WY_MIN + fy * (WY_MAX - WY_MIN)
    return (wx, wy)

def in_viewport(sx: int) -> bool:
    return 0 <= sx < cfg["VP_W"]