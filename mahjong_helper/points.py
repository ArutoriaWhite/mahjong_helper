from collections import namedtuple
import math
from subprocess import CalledProcessError
from mahjong_helper.tile import TilesAndCond
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
        if yaku._group_type(g) == 1 and fl:
            f = 2
        if yaku._group_type(g) == 1 and not fl:
            f = 4
        if yaku._group_type(g) == 2 and fl:
            f = 8
        if yaku._group_type(g) == 2 and not fl:
            f = 16
        if yaku._is_yao_jiu_pai(g[0]):
            f *= 2
        fu += f

    if yaku._is_san_yuan_pai(gtac.eye[0]):
        fu += 2
    if yaku._tile_num(gtac.eye[0]) == gtac.zi_fong:
        fu += 2
    if yaku._tile_num(gtac.eye[0]) == gtac.chang_fong:
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

    Return (0,0,0,0,0,[]) if no yaku
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


def highest_point(ftac: TilesAndCond) -> RonResult:
    """
    ftac: full tiles and cond
    """
    pass
