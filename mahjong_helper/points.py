from audioop import reverse
from collections import namedtuple
from configparser import NoOptionError
from copy import deepcopy
import math
from optparse import Option
from re import I
from subprocess import CalledProcessError
from typing import Optional
from mahjong_helper.tile import TileGroup, TilesAndCond
from mahjong_helper.yaku import HONORS, tile_num, tile_suit
import yaku


def calc_fu(gtac: TilesAndCond) -> int:
    if yaku.qi_dui_zi(gtac) > 0:
        return 25
    if yaku.ping_he(gtac) > 0:
        if gtac.is_tsumo:
            return 20
        else:
            return 30

    fu = 0

    for g, fl in gtac.group_tiles:
        f = 0
        if yaku.group_type(g) == 1 and fl:
            f = 2
        elif yaku.group_type(g) == 1 and not fl:
            f = 4
        elif yaku.group_type(g) == 2 and fl:
            f = 8
        elif yaku.group_type(g) == 2 and not fl:
            f = 16
        if yaku.is_yao_jiu_pai(g[0]):
            f *= 2
        fu += f

    if yaku.is_san_yuan_pai(gtac.eye[0]):
        fu += 2
    if yaku.tile_num(gtac.eye[0]) == gtac.zi_fong:
        fu += 2
    if yaku.tile_num(gtac.eye[0]) == gtac.chang_fong:
        fu += 2

    if gtac.group_ting <= 1:
        fu += 2

    if gtac.is_tsumo:
        fu += 2

    if gtac.is_tsumo or not gtac.is_men_qing:
        return 20+fu
    else:
        return 30+fu


def calc_fan(gtac: TilesAndCond) -> tuple[int, list[tuple[int, str]]]:
    """
    Return (fan, [(fan_1,yaku_name_1), (fan_2,yaku_name_2), ...]

    Return (0,[]) if no yaku
    """
    yakumans: list[tuple[int, str]] = []
    normals: list[tuple[int, str]] = []
    dora = 0

    for i, y in enumerate(yaku.yaku_checkers):
        f = y(gtac)
        if f <= 0:
            continue
        if yaku.yaku_names[i] == 'dora':
            dora += f
        elif yaku.yaku_names[i] in yaku.yakumans:
            yakumans.append((f, yaku.yaku_names[i]))
        else:
            normals.append((f, yaku.yaku_names[i]))

    if len(yakumans) > 0:
        return (sum([f for f, y in yakumans]), yakumans)
    if len(normals) > 0:
        normals.append((dora, 'dora'))
        return (sum([f for f, y in normals]), normals)
    return (0, [])


def calc_basic(fan: int, fu: int) -> int:
    """fan must be > 0"""
    fan_level = [5, 7, 10, 12]
    fan2points = [min(fu*(2**(fan+2)), 2000), 3000, 4000, 6000, 8000]

    for i, f in enumerate(fan_level):
        if fan <= f:
            return fan2points[i]
    return 0


def ceil_to_hundred(x) -> int:
    return (((x-1)//100)+1)*100


RonResult = namedtuple('RonResult', 'basic ron tsumo fan fu yakus')


def grouped_tile_points(gtac: TilesAndCond) -> RonResult:
    """
    Return (basic, ron, tsumo, fan, fu, [(fan_1,yaku_name_1), (fan_2,yaku_name_2), ...])

    Return (0, 0, 0, 0, 0, []) if no yaku
    """
    fan, yakus = calc_fan(gtac)
    fu = calc_fu(gtac)
    b = calc_basic(fan, fu)
    if fan > 0:
        if gtac.is_qin:
            return RonResult(
                b,
                ceil_to_hundred(b*6),
                ceil_to_hundred(b*2),
                fan,
                fu,
                yakus
            )
        else:
            return RonResult(
                b,
                ceil_to_hundred(b*4),
                (ceil_to_hundred(b*2), ceil_to_hundred(b*1)),
                fan,
                fu,
                yakus
            )
    return RonResult(0, 0, 0, 0, 0, [])


def get_shun_from_last(ugtac: TilesAndCond) -> Optional[TilesAndCond]:
    ft = ugtac.free_tiles
    st = ft[-1]
    if (tile_suit(ft[-1]) != tile_suit(ft[-2])
        or tile_suit(ft[-2]) != tile_suit(ft[-3])):
        return None    
    if yaku.tile_suit(st) == HONORS:
        return None

    shun_pos = []
    i = 0
    for j in range(len(ft),0,-1):
        if yaku.tile_suit(ft[j-1]) != yaku.tile_suit(st) or i>2:
            break
        if yaku.tile_num(ft[j-1]) == int(tile_num(st))+i:
            shun_pos.append(j)
            i += 1

    if len(shun_pos) == 3:
        newtac = deepcopy(ugtac)
        newtac.group_tiles.append(TileGroup([],0))
        for i in shun_pos:
            newtac.group_tiles[-1].tiles.append(newtac.free_tiles.pop(i))
        return newtac       # it should not be gc
    else:
        return None


def get_ke_from_last(ugtac: TilesAndCond) -> Optional[TilesAndCond]:
    ft = ugtac.free_tiles
    if (tile_suit(ft[-1]) != tile_suit(ft[-2])
        or tile_suit(ft[-2]) != tile_suit(ft[-3])):
        return None    
    if (ft[-1] == ft[-2] and ft[-2] == ft[-3]):
        newtac = deepcopy(ugtac)
        newtac.group_tiles.append(TileGroup([
            newtac.free_tiles.pop(),
            newtac.free_tiles.pop(),
            newtac.free_tiles.pop()
        ],0))
        return newtac
    return None


def all_grouped_ways(ugtac: TilesAndCond, res: list[TilesAndCond]):
    """
    ugtac:

        free tiles: sort by suits, sort by number, reverse
    """
    if len(ugtac.free_tiles) < 3:
        res.append(deepcopy(ugtac))
        return

    newtac = get_ke_from_last(ugtac)
    if newtac:
        all_grouped_ways(newtac,res)

    newtac = get_shun_from_last(ugtac)
    if newtac:
        all_grouped_ways(newtac,res)



def highest_point(ungrouped_14_tac: TilesAndCond) -> RonResult:
    """
    may not in win pattern, but it's ready to win
    """
    ungrouped_14_tac.free_tiles.sort(reverse=True)
    ways = list()
    all_grouped_ways(ungrouped_14_tac, ways)

    res = RonResult(0,0,0,0,0,[])
    for gtac in ways:
        ron = grouped_tile_points(gtac)
        if ron.basic > res.basic:
            res = ron
    return res


    
    
"""
calc free_cnt(ungrouped_13_tac as u13tac):
    enum last tile as lt
        if hands + lt can hu
            free_cnt ++

---

all_grouped_ways(ungrouped_full_cnt uftac)

highest_point(ungrouped_full_tac as uftac)
    enum gtac in all_grouped_ways(uftac):
        # gtac grouped_ting_cnt is set
        res = max(res, grouped_tile_points(gtac))

ting_what(ungrouped_13_tac as u13tac):
    res
    enum last tile as lt
        uftac = u13tac+lt
        res.append(highest_point(uftac))
"""
