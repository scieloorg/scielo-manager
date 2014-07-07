# coding: utf-8
def validate_sequence(sequence, open_symbol='SERV_BEGIN', close_symbol='SERV_END'):
    opened = 0
    for item in sequence:
        if item == open_symbol:
            opened += 1
        elif item == close_symbol:
            opened -= 1

        if opened < 0:  # quebra a invariante
            return False

    return opened == 0