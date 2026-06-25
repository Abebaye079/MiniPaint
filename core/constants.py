# World coordinate range
WX_MIN, WX_MAX = -10.0,  10.0
WY_MIN, WY_MAX =  -7.2,   7.2

# Layout
SIDEBAR   = 200
VP_X, VP_Y = 0, 0

# Mutable window state
cfg = {
    "WIN_W": 1000,
    "WIN_H": 680,
    "VP_W":  1000 - SIDEBAR,   # 800
    "VP_H":  680,
}

# Colour palette
PALETTE = [
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.0, 0.85,0.0),
    (0.1, 0.3, 1.0),
    (1.0, 0.85,0.0),
    (1.0, 0.45,0.0),
    (0.6, 0.0, 1.0),
    (0.0, 0.85,0.9),
    (1.0, 0.4, 0.7),
    (1.0, 1.0, 1.0),
]

# Transform step sizes
TSTEP = 0.20    # translation
RSTEP = 5.0     # rotation
SSTEP = 0.05    # scale