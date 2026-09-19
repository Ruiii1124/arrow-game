# levels.py - 关卡数据（0=上 1=右 2=下 3=左）
LEVELS = [
    # 关卡 1：4x4，4 个箭头
    # 通关：(1,1)↑ → (2,0)← → (0,2)→ → (3,3)→
    [
        [None, None, 1,    None],
        [None, 0,    None, None],
        [3,    None, None, None],
        [None, None, None, 1],
    ],

    # 关卡 2：4x4，4 个箭头
    [
        [0,    None, None, None],
        [None, None, 1,    None],
        [3,    None, None, 2],
        [None, None, None, None],
    ],

    # 关卡 3：5x5，9 个箭头
    [
        [0,    None, 1,    None, 0],
        [None, None, None, None, None],
        [3,    None, 2,    None, 1],
        [None, None, None, None, None],
        [2,    None, 3,    None, 2],
    ],
]