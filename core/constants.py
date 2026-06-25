# World coordinate range
WX_MIN, WX_MAX = -10.0,  10.0
WY_MIN, WY_MAX =  -7.2,   7.2

# Layout
SIDEBAR   = 200          # right panel width  (pixels)
VP_X, VP_Y = 0, 0       # viewport origin

# Mutable window state  
cfg = {
    "WIN_W": 1000,
    "WIN_H": 680,
    "VP_W":  1000 - SIDEBAR,   # 800
    "VP_H":  680,
}

# Colour palette 
PALETTE = [
    (0.0, 0.0, 0.0),   # 0 black
    (1.0, 0.0, 0.0),   # 1 red
    (0.0, 0.85,0.0),   # 2 green
    (0.1, 0.3, 1.0),   # 3 blue
    (1.0, 0.85,0.0),   # 4 yellow
    (1.0, 0.45,0.0),   # 5 orange
    (0.6, 0.0, 1.0),   # 6 purple
    (0.0, 0.85,0.9),   # 7 cyan
    (1.0, 0.4, 0.7),   # 8 pink
    (1.0, 1.0, 1.0),   # 9 white
]

# Transform step sizes 
TSTEP = 0.20    # translation 
RSTEP = 5.0     # rotation    
SSTEP = 0.05    # scale       