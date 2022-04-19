import collections
import math
import yaku

#tiles classes En naming reference to https://github.com/Camerash/mahjong-dataset
#aka dora example: dots-8-r
#normal example: dots-8-n

class TilesAndCond:
    def __init__ (self) -> None:
        """
        grouped_tiles:
            eye in last
            shun is sorted
        """
        self.all_tiles: list[str]
        self.free_tiles: list[str]
        TilesGroup = collections.namedtuple('TileGroup','tiles is_fu_lou')
        self.group_tiles: list[TilesGroup] #eye in last
        self.ting_count: int
        self.is_tsumo: bool
        self.is_ron = not self.is_tsumo
        self.chang_fong: str
        self.zi_fong: str
        self.doras: dict[str,int] #which dora, count
        self.is_riichi: bool
        self.is_double_riichi: bool
        self.is_ippatsu: bool
        self.is_chiang_gang: bool
        self.is_ling_shang_kai_hua: bool
        self.is_hai_di_lao_yue: bool
        self.is_he_di_lao_yu: bool
        self.is_tian_hu: bool
        self.is_di_hu: bool
        self.is_qin: bool
        self.is_zi: bool = not self.is_qin

    @property
    def is_men_qing (self) -> bool:
        for g in self.group_tiles:
            if g[1]: #is fu lou
                return False
        return True

    @property
    def eye(self) -> list[str]:
        return self.group_tiles[-1].tiles

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