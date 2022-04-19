import collections
import math
import yaku

def calc_fu (self) -> int:
    if self.yaku_checker.qi_dui_zi()[0]:
        return 25
    if  self.yaku_checker.ping_he()[0]:
        if self.grouped_tiles_and_cond.is_tsumo:
            return 20
        else:
            return 30
    fu = 0
    if self.grouped_tiles_and_cond.is_tsumo or self.grouped_tiles_and_cond.is_men_qing:
        return 20+fu
    else:
        return 30+fu

def calc_fan (self) -> tuple[int,list[tuple[int,str]]]:
    pass

def calc_basic (self) -> int:
    fan_level = [5, 7, 10, 12]
    fan2points = [min(self.fu*(2**(self.fan+2)),2000), 3000, 4000, 6000, 8000]
    
    points = 0
    for i,f in enumerate(fan_level):
        if self.fan <= f:
            points = fan2points[i]
            break
    return points

def ceil_to_hundred (self,x) -> int:
    return (((x-1)//100)+1)*100

def has_yakus (self) -> bool:
    for y in self.yakus:
        if y != 'dora' and y != 'aka dora':
            return True
    return False

"""
def grouped_tiles_points () -> dict:
    if not self.has_yakus():
        return {
            "ron":0,
            "tsumo":0,
            "yakus":[]
        }

    if self.grouped_tiles_and_cond.is_qin:
        return {
            "ron":self.ceil_to_hundred(self.b*6),
            "tsumo":self.ceil_to_hundred(self.b*2),
            "yakus":self.yakus
        }
    else:
        return {
            "ron":self.ceil_to_hundred(self.b*4),
            "tsumo":(self.ceil_to_hundred(self.b*2),self.ceil_to_hundred(self.b*1)),
            "yakus":self.yakus
        }
"""


def highest_point () -> dict:
    pass