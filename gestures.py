gestures = dict([
    (0, 'A'),
    (1, 'B'),
    (2, 'C'),
    (3, 'D'),
    (4, 'E'),
    (5, 'F'),
    (6, 'G'),
    (7, 'H'),
    (8, 'I'),
    (9, 'J'),
    (10, 'K'),
    (11, 'L'),
    (12, 'M'),
    (13, 'N'),
    (14, 'O'),
    (15, 'P'),
    (16, 'Q'),
    (17, 'R'),
    (18, 'S'),
    (19, 'T'),
    (20, 'U'),
    (21, 'V'),
    (22, 'W'),
    (23, 'X'),
    (24, 'Y'),
    (25, 'razmak'),
    (26, 'obrisi'),
    (27, '1'),
    (28, '2'),
    (29, '3'),
    (30, '4'),
    (31, '5'),
    (32, '6'),
    (33, '7'),
    (34, '8'),
    (35, '9'),
    (36, 'CH'),
    (37, 'Ć'),
    (38, 'DŽ'),
    (39, 'Đ'),
    (40, 'Z'),
    (41, 'srce'),
    (42, 'fuck'),
    (43, 'metal'),#override
    (44, 'Z'),
    (45, 'A'),
    (46, 'B'),
    (47, 'C'),
    (48, 'D'),
    (49, 'E'),
    (50, 'F'),
    (51, 'G'),
    (52, 'H'),
    (53, 'I'),
    (54, 'J'),
    (55, 'K'),
    (56, 'L'),
    (57, 'O'),
    (58, 'P'),
    (59, 'R'),
    (60, 'S'),
    (61, 'T'),
    (62, 'U'),
    (63, 'V')
])

"""
helping function for getting the letter representation of the gesture
"""
def get_pred_text(pred_class):
    return gestures[pred_class]

def add_gesture(g_id, g_name):
    gestures[g_id]=g_name

#print(get_pred_text(2))
#print(get_pred_text(15))
