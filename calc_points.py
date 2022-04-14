from pdb import post_mortem
import math
import yi

class Conditions:
    is_qin = 1

def get_fu (splited_tiles, conditions):
    if yi.is_qi_dui_zi():
        return 25
    if  yi.is_ping_he():
        if conditions.is_tsumo:
            return 20
        else:
            return 30
    
    fu = 0

    if conditions.is_tsumo or conditions.is_men_qing:
        return 20+fu
    else:
        return 30+fu
        

def get_fan (splited_tiles, conditions):
    return 2

def get_basic (fu, fan):
    fan_level = [5, 7, 10, 12]
    fan2points = [min(fu*(2**(fan+2)),2000), 3000, 4000, 6000, 8000]
     
    points = 0
    for i,f in enumerate(fan_level):
        if fan <= f:
            points = fan2points[i]
            break
    return points

def ceil_to_hundred (x):
    return (((x-1)//100)+1)*100

def calc_points (splited_tiles, conditions):
    fu = get_fu(splited_tiles, conditions)
    fan = get_fan(splited_tiles, conditions)

    b = get_basic(fu,fan)
    
    if conditions.is_qin:
        return {"ron":ceil_to_hundred(b*6), "tsumo":ceil_to_hundred(b*2)}
    else:
        return {"ron":ceil_to_hundred(b*4), "tsumo":(ceil_to_hundred(b*2),ceil_to_hundred(b*1))}

print(calc_points([], Conditions()))