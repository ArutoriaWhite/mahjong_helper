import math

class TilesAndConditions:
    def __init__ (self):
        self.free_tiles = []
        self.group_tiles = []
        self.is_tsumo
        self.is_ron = not self.is_tsumo
        self.chang_fong
        self.zi_fong
        self.doras
        self.is_riichi
        self.is_double_riichi
        self.is_ippatsu
        self.is_chiang_gang
        self.is_ling_shang_kai_hua
        self.is_hai_di_lao_yue
        self.is_tian_hu
        self.is_di_hu
        self.is_qin
        self.is_zi = not self.is_qin
        
    @property
    def is_men_qing (self):
        pass

class YakuChecker:
    pass

class PointsCaculator:
    def __init__ (self, _grouped_tiles_and_cond):
        self.grouped_tiles_and_cond = _grouped_tiles_and_cond
        self.yaku = YakuChecker(TilesAndConditions)
        self.fu = self.get_fu()
        self.fan = self.get_fan()
        self.b = self.get_basic()

    def get_fu (self):
        if self.yaku.is_qi_dui_zi():
            return 25
        if  self.yaku.is_ping_he():
            if self.grouped_tiles_and_cond.is_tsumo:
                return 20
            else:
                return 30
        fu = 0

        if self.grouped_tiles_and_cond.is_tsumo or self.grouped_tiles_and_cond.is_men_qing:
            return 20+fu
        else:
            return 30+fu

    def get_fan (self):
        return 2

    def get_basic (self):
        fan_level = [5, 7, 10, 12]
        fan2points = [min(self.fu*(2**(self.fan+2)),2000), 3000, 4000, 6000, 8000]
        
        points = 0
        for i,f in enumerate(fan_level):
            if self.fan <= f:
                points = fan2points[i]
                break
        return points

    def ceil_to_hundred (self,x):
        return (((x-1)//100)+1)*100

    def get_points (self):
        b = self.b
        if self.grouped_tiles_and_cond.is_qin:
            return {"ron":self.ceil_to_hundred(b*6), "tsumo":self.ceil_to_hundred(b*2)}
        else:
            return {"ron":self.ceil_to_hundred(b*4), "tsumo":(self.ceil_to_hundred(b*2),self.ceil_to_hundred(b*1))}

def highest_point ():
    pass