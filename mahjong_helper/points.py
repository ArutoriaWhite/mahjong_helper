import math
from collections import defaultdict, namedtuple
from copy import deepcopy
from typing import Optional

import yaku
from tile import *


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
        if yaku.group_type(g) == 1:
            f = 2
        elif yaku.group_type(g) == 2:
            f = 8
        if not fl:
            f *= 2
        if yaku.is_yao_jiu_pai(g[0]):
            f *= 2
        fu += f

    if yaku.is_san_yuan_pai(gtac.eye[0]):
        fu += 2
    if yaku.tile_num(gtac.eye[0]) == gtac.zi_fong:
        fu += 2
    if yaku.tile_num(gtac.eye[0]) == gtac.chang_fong:
        fu += 2

    if gtac.ting_cnt <= 1:
        fu += 2

    if gtac.is_tsumo:
        fu += 2

    fu = max(fu, 1)
    if gtac.is_tsumo or not gtac.is_men_qing:
        return ceil_to(20+fu, 10)
    else:
        return ceil_to(30+fu, 10)


def calc_fan(gtac: TilesAndCond) -> tuple[int, list[tuple[int, str]]]:
    """
    Return (total_fan, [(fan_1,yaku_name_1), (fan_2,yaku_name_2), ...]

    Return (0,[]) if no yaku
    """
    yakumans: list[tuple[int, str]] = []
    normals: list[tuple[int, str]] = []
    dora = 0

    for i, y in enumerate(yaku.YAKU_CHECKERS):
        f = y(gtac)
        if f <= 0:
            continue
        if yaku.YAKU_NAMES[i] == 'dora':
            dora += f
        elif yaku.YAKU_NAMES[i] in yaku.YAKUMANS:
            yakumans.append((f, yaku.YAKU_NAMES[i]))
        else:
            normals.append((f, yaku.YAKU_NAMES[i]))

    if len(yakumans) > 0:
        return (sum([f for f, y in yakumans]), yakumans)
    if len(normals) > 0:
        if dora > 0:
            normals.append((dora, 'dora'))
        return (sum([f for f, y in normals]), normals)
    return (0, [])


def calc_basic(fan: int, fu: int) -> int:
    """fan must be > 0"""
    assert(fan > 0)
    fan_level = [5, 7, 10, 12]
    fan2points = [min(fu*(2**(fan+2)), 2000), 3000, 4000, 6000]

    for i, f in enumerate(fan_level):
        if fan <= f:
            return fan2points[i]
    return fan//13*8000


def ceil_to(x, y) -> int:
    return (((x-1)//y)+1)*y


RonResult = namedtuple('RonResult', 'basic ron tsumo fan fu yakus')


def grouped_tile_points(gtac: TilesAndCond) -> RonResult:
    fan, yakus = calc_fan(gtac)
    fu = calc_fu(gtac)
    b = calc_basic(fan, fu)
    if fan > 0:
        if gtac.is_qin:
            return RonResult(
                b,
                ceil_to(b*6, 100),
                ceil_to(b*2, 100),
                fan,
                fu,
                yakus
            )
        else:
            return RonResult(
                b,
                ceil_to(b*4, 100),
                (ceil_to(b*2, 100), ceil_to(b*1, 100)),
                fan,
                fu,
                yakus
            )
    return RonResult(0, 0, 0, 0, 0, [])


def get_shun_from_last(ugtac: TilesAndCond) -> Optional[TilesAndCond]:
    """
    assert ugtac.free_tiles is sorted
    """
    ft = ugtac.free_tiles

    if yaku.tile_suit(ft[-1]) == yaku.HONORS:
        return None

    shun_pos = []
    i = 0
    for j in range(len(ft)-1, -1, -1):
        if yaku.tile_suit(ft[j]) != yaku.tile_suit(ft[-1]) or i > 2:
            break
        if yaku.tile_num(ft[j]) == int(yaku.tile_num(ft[-1]))+i:
            shun_pos.append(j)
            i += 1

    if len(shun_pos) == 3:
        newtac = deepcopy(ugtac)
        newtac.group_tiles.append(TileGroup([], 0))
        for i in shun_pos:
            newtac.group_tiles[-1].tiles.append(newtac.free_tiles.pop(i))
        return newtac       # it should not be gc
    else:
        return None


def get_ke_from_last(ugtac: TilesAndCond) -> Optional[TilesAndCond]:
    ft = ugtac.free_tiles
    if (yaku.tile_suit(ft[-1]) != yaku.tile_suit(ft[-2])
            or yaku.tile_suit(ft[-2]) != yaku.tile_suit(ft[-3])):
        return None
    if (ft[-1] == ft[-2] and ft[-2] == ft[-3]):
        newtac = deepcopy(ugtac)
        newtac.group_tiles.append(TileGroup([
            newtac.free_tiles.pop(),
            newtac.free_tiles.pop(),
            newtac.free_tiles.pop()
        ], 0))
        return newtac
    return None


def calc_grouped_ting_cnt(ugtac: TilesAndCond) -> set[int]:
    # 對於一組分組方法，遍歷每個沒有副漏（除了暗槓）＆＆含有最後一張牌的組，檢查組內牌型，聽牌數取小的
    res: set[int] = set()
    for g, fl in ugtac.group_tiles:

        if fl or yaku.group_type(g) == 2 or ugtac.last_tile not in g:
            continue
        if yaku.group_type(g) == 0:
            # 1,2,* or *,8,9
            # x,*,x+2
            # x,x+1,*
            nums = [int(yaku.tile_num(t)) for t in g if t != ugtac.last_tile]
            if nums == [1, 2] or nums == [8, 9]:
                res.add(1)
            elif nums[0]+1 == nums[1]:
                res.add(2)
            else:
                res.add(1)
        elif yaku.group_type(g) == 1:
            res.add(2)
        elif yaku.group_type(g) == 3:
            res.add(1)
    return res


def group_normally(ugtac: TilesAndCond, res: list[TilesAndCond]):
    ft = ugtac.free_tiles
    ft.sort(reverse=True)

    def dfs(ugtac: TilesAndCond, res: list[TilesAndCond]):
        """
        ugtac:

            free tiles: sort by suits, sort by number, reverse
        """
        if len(ugtac.free_tiles) < 3:
            res.append(ugtac)
            return

        newtac = get_ke_from_last(ugtac)
        if newtac:
            dfs(newtac, res)

        newtac = get_shun_from_last(ugtac)
        if newtac:
            dfs(newtac, res)

    ress = set()
    eye = None
    for i in range(len(ft)-1, -1, -1):
        if (eye is None or eye.tiles[0] != ft[i]) and ft[i] == ft[i-1]:
            newtac = deepcopy(ugtac)
            eye = TileGroup([newtac.free_tiles.pop(
                i), newtac.free_tiles.pop(i-1)], 0)
            # newtac.print_content()
            ways: list[TilesAndCond] = []
            dfs(newtac, ways)
            for w in ways:
                w.group_tiles.append(eye)
                for tcnt in calc_grouped_ting_cnt(w):
                    way_with_different_tcnt = deepcopy(w)
                    way_with_different_tcnt.ting_cnt = tcnt
                    ress.add(way_with_different_tcnt)
    res.extend(list(ress))


def group_qi_dui_zi(ugtac: TilesAndCond, res: list[TilesAndCond]):
    ugtac.free_tiles.sort(reverse=True)
    if len(ugtac.free_tiles) != 14:
        return
    newtac = deepcopy(ugtac)
    while len(newtac.free_tiles) > 0:
        eye = [newtac.free_tiles.pop(), newtac.free_tiles.pop()]
        if eye[0] != eye[1]:
            return
        newtac.group_tiles.append(TileGroup(eye, 0))
    res.append(newtac)


def group_guo_shi_wu_shuang(ugtac: TilesAndCond, res: list[TilesAndCond]):
    ugtac.free_tiles.sort(reverse=True)
    if len(ugtac.free_tiles) != 14:
        return
    # 出現 13 張牌 + 一張重複
    # 13 group
    # 是否是國士
    # 是國士：iterator sorted free tiles, put into newtac grouped
    GUO_SHI = {
        f'{DOTS}-1', f'{DOTS}-9', f'{BAMBOO}-1', f'{BAMBOO}-9', f'{CHARACTERS}-1', f'{CHARACTERS}-9',
        f'{HONORS}-{EAST}', f'{HONORS}-{SOUTH}', f'{HONORS}-{WEST}', f'{HONORS}-{NORTH}',
        f'{HONORS}-{RED}', f'{HONORS}-{GREEN}', f'{HONORS}-{WHITE}',
    }
    if set(ugtac.all_tiles) != GUO_SHI:
        return
    newtac = deepcopy(ugtac)
    while len(newtac.free_tiles) > 0:
        newtac.group_tiles.append(TileGroup([], 0))
        newtac.group_tiles[-1].tiles.append(newtac.free_tiles.pop())
        if len(newtac.free_tiles) and newtac.group_tiles[-1].tiles[0] == newtac.free_tiles[-1]:
            newtac.group_tiles[-1].tiles.append(newtac.free_tiles.pop())
    res.append(newtac)


def highest_point(ungrouped_14_tac: TilesAndCond) -> RonResult:
    """
    may not in win pattern, but it's ready to win
    """
    ways: list[TilesAndCond] = list()
    group_normally(ungrouped_14_tac, ways)
    group_qi_dui_zi(ungrouped_14_tac, ways)
    group_guo_shi_wu_shuang(ungrouped_14_tac, ways)

    res = RonResult(0, 0, 0, 0, 0, [])
    for gtac in ways:
        ron = grouped_tile_points(gtac)
        if ron.basic > res.basic:
            res = ron
    return res


def find_last_tile(ungroup_13_tac: TilesAndCond) -> tuple[RonResult, str]:
    res = RonResult(0, 0, 0, 0, 0, [])
    last_tile = ''
    for t in TILES:
        tac = deepcopy(ungroup_13_tac)
        tac.free_tiles.append(t)
        tac.last_tile = t
        ron = highest_point(tac)
        if ron.basic > res.basic:
            res = ron
            last_tile = t
    return (res, last_tile)


# if __name__ == '__main__':        # testing ouob
#     gtac = TilesAndCond()
#     gtac.free_tiles = [
#         f'{CHARACTERS}-9', f'{CHARACTERS}-9',
#         '-white', 'honors-white', 'honors-white',
#         'honors-red', 'honors-red', 'honors-red',
#     ]
#     gtac.group_tiles = [
#         TileGroup(['b-3', 'b-4', 'b-5'], 1),
#         TileGroup(['honors-green', 'honors-green', 'honors-green'], 1)
#     ]
#     gtac.last_tile = 'honors-red'
#     gtac.is_tsumo = False
#     gtac.is_ippatsu = False
#     gtac.is_riichi = False
#     #gtac.doras['honors-north'] = 1
#     #gtac.aka_doras = []
#     gtac.chang_fong = 'east'
#     gtac.zi_fong = 'east'

#     gtac.free_tiles.sort(reverse=True)
#     # res = get_shun_from_last(gtac)
#     # if res:
#     #     res.print_content()
#     # else:
#     #     eprint('none')

#     res: list[TilesAndCond] = []
#     normal_grouped_way(gtac, res)
#     group_guo_shi_wu_shuang(gtac, res)
#     group_qi_dui_zi(gtac, res)
#     for r in res:
#         r._print_content()
#         print(grouped_tile_points(r))
