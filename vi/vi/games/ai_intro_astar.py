import string

def map_type_to_value(type):
    if   type == 'w': return 100
    elif type == 'm': return 50
    elif type == 'f': return 10
    elif type == 'g': return 5
    elif type == 'r': return 1
    else: raise ValueError('invalid map type: ' + type)

def map_value_to_type(value):
    if value == 100: return 'w'
    elif value == 50: return 'm'
    elif value == 10: return 'f'
    elif value == 5: return 'g'
    elif value == 1: return 'r'
    else: raise ValueError('invalid map value: ' + value)

class ai_intro_astar(object):
    def __init__(self):
        for a in string.ascii_lowercase:
            try:
                print("{0}".format(map_type_to_value(a))
            except:
                pass
