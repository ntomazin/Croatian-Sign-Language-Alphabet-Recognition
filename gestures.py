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
    (25, 'nezz'),
    (26, 'nezz'),
    (27, '1'),
    (28, '2'),
    (29, '3'),
    (30, '4'),
    (31, '5'),
    (32, '6'),
    (33, '7'),
    (34, '8'),
    (35, '9'),
    (36, 'nezz'),
    (37, 'nezz'),
    (38, 'nezz'),
    (39, 'nezz'),
    (40, 'nezz'),
    (41, 'LJUBAV'),
    (42, 'FAKIC'),
    (43, 'ROCK')
    ])

"""
helping function for getting the letter representation of the gesture
"""
def get_pred_text(pred_class):
    return gestures[pred_class]

#print(get_pred_text(2))
#print(get_pred_text(15))
