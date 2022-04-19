from collections import defaultdict
from ctypes import Union
from email.policy import default
from operator import gt
from tokenize import group
from typing import Optional
from points import TilesAndCond
from calc import *

HONORS = 'honors'

########### decorators #################


def men_qing_only(func):
    def wrapper(gtac: TilesAndCond):
        if gtac.is_men_qing:
            return func(gtac)
        return 0
    return wrapper


def fu_lou_minus_one(func):
    def wrapper(gtac: TilesAndCond):
        return func(gtac)-gtac.is_men_qing
    return wrapper


def high_level_yaku(higher_yaku):
    def deco(func):
        def wrapper(gtac: TilesAndCond):
            hy = higher_yaku(gtac)
            return hy if hy>0 else func(gtac)
        return wrapper
    return deco

############### tile and group info ################


def tile_suit(tile: str) -> str:
    return tile.split('-')[0]


def tile_num(tile: str) -> int | str:
    if tile_suit(tile) == HONORS:
        return tile.split('-')[1]
    return int(tile.split('-')[1])


def is_zi_pai(tile: str) -> bool:
    return tile_suit(tile) == HONORS


def is_lao_tou_pai(tile: str) -> bool:
    return tile_num(tile) == 1 or tile_num(tile) == 9


def is_yao_jiu_pai(tile: str) -> bool:
    return is_zi_pai(tile) or is_lao_tou_pai(tile)


def is_san_yuan_pai(tile: str) -> bool:
    s = {'green', 'red', 'white'}
    return tile_num(tile) in s


def is_feng_pai(tile: str) -> bool:
    s = {'east', 'south', 'west', 'north'}
    return tile_num(tile) in s


def group_type(tiles: list[str]) -> int:
    """
    return
        0: shun
        1: ke
        2: gang
        3: eye
        -1: not either
    """

    if [tile_suit(t) for t in tiles].count(tile_suit(tiles[0])) != len(tiles):      #all type must be same
        return -1
    if tile_suit(tiles[0]) != HONORS and len(tiles) == 3:
        nums = sorted([int(tile_num(t)) for t in tiles])
        if nums[0]+1 == nums[1] and nums[1]+1 == nums[2]:
            return 0
    if len(tiles) == 3 and tiles.count(tiles[0]) == 3:
        return 1
    if len(tiles) == 4 and tiles.count(tiles[0]) == 4:
        return 2
    if len(tiles) == 2 and tiles.count(tiles[0]) == 2:
        return 3
    return -1


################ yakus ###############

# TODO:
# - check requirements is to strict, like er_bei_kou 3 shun


def dora(gtac: TilesAndCond) -> int:
    """Return sum of every type of dora"""
    sum = 0
    for t in gtac.all_tiles:
        sum += gtac.doras[f'{tile_suit(t)}-{tile_num(t)}']
        sum += t[-1] == 'r'
    return sum


def duan_yao_jiu(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not is_yao_jiu_pai(t):
            return 0
    return 1


def chiang_gang(gtac: TilesAndCond) -> int:
    return gtac.is_chiang_gang*1


def ling_shang_kai_hua(gtac: TilesAndCond) -> int:
    return gtac.is_ling_shang_kai_hua*1


def hai_di_lao_yue(gtac: TilesAndCond) -> int:
    return gtac.is_hai_di_lao_yue*1


def he_di_lao_yu(gtac: TilesAndCond) -> int:
    return gtac.is_he_di_lao_yu*1


def ippatsu(gtac: TilesAndCond) -> int:
    return gtac.is_ippatsu*1


@men_qing_only
def men_qing_tsumo(gtac: TilesAndCond) -> int:
    return gtac.is_tsumo*1


@men_qing_only
def ping_he(gtac: TilesAndCond) -> int:
    for g in gtac.group_tiles:
        if group_type(g.tiles) != 0:
            return 0
    yi_pai = {
        gtac.chang_fong,
        gtac.zi_fong,
        'red', 'white', 'green'
    }
    if tile_num(gtac.eye[0]) in yi_pai and gtac.ting_count == 2:
        return 1
    return 0


def chang_feng_pai(gtac: TilesAndCond) -> int:
    for g in gtac.group_tiles:
        if group_type(g.tiles) in {1, 2} and tile_num(g.tiles[0]) == gtac.chang_fong:
            return 1
    return 0


def zi_feng_pai(gtac: TilesAndCond) -> int:
    for g in gtac.group_tiles:
        if group_type(g.tiles) in {1, 2} and tile_num(g.tiles[0]) == gtac.zi_fong:
            return 1
    return 0


def san_yuan_pai(gtac: TilesAndCond) -> int:
    sum = 0
    for g in gtac.group_tiles:
        if group_type(g.tiles) in {1, 2} and is_san_yuan_pai(g.tiles[0]):
            sum += 1
    return sum


def xiao_san_yuan(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    eye_cnt = 0
    for g in gtac.group_tiles:
        if group_type(g.tiles) in {1, 2} and is_san_yuan_pai(g.tiles[0]):
            ke_cnt += 1
        if group_type(g.tiles)==3 and is_san_yuan_pai(g.tiles[0]):
            eye_cnt += 1

    return (ke_cnt == 2 and eye_cnt == 1)*2


def san_gang_zi(gtac: TilesAndCond) -> int:
    cnt = 0
    for g in gtac.group_tiles:
        if group_type(g.tiles) == 2:
            cnt += 1
    return (cnt == 3)*2


def hun_lao_tou(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not is_yao_jiu_pai(t):
            return 0
    return 2


def san_an_ke(gtac: TilesAndCond) -> int:
    cnt = 0
    for g, fl in gtac.group_tiles:
        if (not fl) and group_type(g) in {1, 2}:
            cnt += 1
    return (cnt == 3)*2


def dui_dui_he(gtac: TilesAndCond) -> int:
    cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2}:
            cnt += 1
    return (cnt == 4)*2


def san_se_tong_ke(gtac: TilesAndCond) -> int:
    num_cnt = defaultdict(int)
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and tile_suit(g[0]) != HONORS:
            num_cnt[tile_num(g[0])] += 1
    for k, v in num_cnt:
        if v == 3:
            return 3
    return 0


@fu_lou_minus_one
def san_se_tong_shun(gtac: TilesAndCond) -> int:
    types = defaultdict(set)
    for g, fl in gtac.group_tiles:
        if group_type(g) == 0 and tile_suit(g[0]) != HONORS:
            types[tile_num(g[0])].add(tile_suit(g[0]))
    for k, v in types:
        if len(v):
            return 3
    return 0


@fu_lou_minus_one
def yi_qi_tong_guan(gtac: TilesAndCond) -> int:
    shun = defaultdict(set)
    for g, fl in gtac.group_tiles:
        if group_type(g) == 0 and tile_suit(g[0]) != HONORS:
            if not tile_suit(g[0]) in shun:
                shun[tile_suit(g[0])].add(tile_num(g[0]))
    for k, v in shun:
        if {1, 4, 7}.issubset(v):
            return 2
    return 0


@men_qing_only
def double_riichi(gtac: TilesAndCond) -> int:
    return gtac.is_double_riichi*2


@high_level_yaku(double_riichi)
@men_qing_only
def riichi(gtac: TilesAndCond) -> int:
    return gtac.is_riichi


@men_qing_only
def qi_dui_zi(gtac: TilesAndCond) -> int:
    return (len(gtac.group_tiles) == 7)*2


@fu_lou_minus_one
def chun_quan_dai_yao_jiu(gtac: TilesAndCond) -> int:
    shun_cnt = 0
    ke_cnt = 0
    eye_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and is_lao_tou_pai(g[0]):
            ke_cnt += 1
        if group_type(g) == 0:
            if is_lao_tou_pai(g[0]) or is_lao_tou_pai(g[-1]):
                shun_cnt += 1
        if group_type(g) == 3 and is_lao_tou_pai(g[0]):
            eye_cnt += 1
    if (shun_cnt+ke_cnt) == 4 and shun_cnt > 0 and eye_cnt > 0:
        return 3
    return 0


@high_level_yaku(hun_lao_tou)
@high_level_yaku(chun_quan_dai_yao_jiu)
@fu_lou_minus_one
def hun_quan_dai_yao_jiu(gtac: TilesAndCond) -> int:
    shun_cnt = 0
    ke_cnt = 0
    eye_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and is_yao_jiu_pai(g[0]):
            ke_cnt += 1
        if group_type(g) == 0:
            if is_lao_tou_pai(g[0]) or is_yao_jiu_pai(g[-1]):
                shun_cnt += 1
        if group_type(g) == 3 and is_yao_jiu_pai(g[0]):
            eye_cnt += 1
    if (shun_cnt+ke_cnt) == 4 and shun_cnt > 0 and eye_cnt > 0:
        return 3
    return 0


@men_qing_only
def er_bei_kou(gtac: TilesAndCond) -> int:
    tile_cnt = defaultdict(int)
    for g, fl in gtac.group_tiles:
        if group_type(g) == 0:
            tile_cnt[g[0]] += 1
    yi_bei_kou_cnt = 0
    for k, v in tile_cnt:
        if v >= 2:
            yi_bei_kou_cnt += 1
    if yi_bei_kou_cnt >= 2:
        return 3
    return 0


@high_level_yaku(er_bei_kou)
@men_qing_only
def yi_bei_kou(gtac: TilesAndCond) -> int:
    s = set()
    for g, fl in gtac.group_tiles:
        gt = group_type(g)
        if gt == 0:
            if gt in s:
                return 1
            else:
                s.add(gt)
    return 0

# 6 fan


@fu_lou_minus_one
def qing_yi_se(gtac: TilesAndCond) -> int:
    t = gtac.group_tiles[0].tiles[0]
    for g, fl in gtac.group_tiles:
        if tile_suit(g[0]) == HONORS:
            return 0
        if tile_suit(g[0]) != t:
            return 0
    return t


@high_level_yaku(qing_yi_se)
@fu_lou_minus_one
def hun_yi_se(gtac: TilesAndCond) -> int:
    t = None
    for g, fl in gtac.group_tiles:
        if tile_suit(g[0]) == HONORS:
            continue
        if t:
            if tile_suit(g[0]) != t:
                return 0
        else:
            t = tile_suit(g[0])
    return 3

# double yakuman


def da_si_xi(gtac: TilesAndCond) -> int:
    feng = set()
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and is_feng_pai(g[0]):
            feng.add(g[0])
    if len(feng) == 4:
        return 26
    return 0


def da_san_yuan(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and is_san_yuan_pai(tile_suit(g[0])):
            ke_cnt += 1
    return 13 if ke_cnt >= 3 else 0


def si_gang_zi(gtac: TilesAndCond) -> int:
    gang_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) == 2:
            gang_cnt += 1
    return 13 if gang_cnt >= 4 else 0


def qing_lao_tou(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not is_lao_tou_pai(t):
            return 0
    return 13


def xiao_si_xi(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    eye_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and is_feng_pai(g[0]):
            ke_cnt += 1
        if group_type(g) == 3 and is_feng_pai(g[0]):
            eye_cnt += 1
    return 13 if ke_cnt == 3 and eye_cnt == 1 else 0


def zi_yi_se(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not is_zi_pai(t):
            return 0
    return 13


def lv_yi_se(gtac: TilesAndCond) -> int:
    s = {2, 3, 4, 6, 8}
    for t in gtac.all_tiles:
        if tile_suit(t) == HONORS:
            if tile_num != 'green':
                return 0
        else:
            if tile_suit(t) != 'bamboo' or tile_num(t) not in s:
                return 0
    return 13


@men_qing_only
def si_an_ke_dan_ji(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    if gtac.ting_count > 1:
        return 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and (not fl):
            ke_cnt += 1
    return 26 if ke_cnt >= 4 else 0


@high_level_yaku(si_an_ke_dan_ji)
@men_qing_only
def si_an_ke(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    for g, fl in gtac.group_tiles:
        if group_type(g) in {1, 2} and (not fl):
            ke_cnt += 1
    return 13 if ke_cnt >= 4 else 0


@men_qing_only
def guo_shi_wu_shuang_shi_san_mian(gtac: TilesAndCond) -> int:
    """
    guo shi wu shuang: 12 single + 1 eye
    """
    if gtac.ting_count == 13 and len(gtac.group_tiles) == 13:
        return 26
    return 0


@high_level_yaku(guo_shi_wu_shuang_shi_san_mian)
@men_qing_only
def guo_shi_wu_shuang(gtac: TilesAndCond) -> int:
    """
    guo shi wu shuang: 12 single + 1 eye
    """
    if len(gtac.group_tiles) == 13:
        return 13
    return 0


@men_qing_only
def chun_zheng_jiu_lian_bao_deng(gtac: TilesAndCond) -> int:
    t = tile_suit(gtac.all_tiles[0])
    num = []
    for x in gtac.all_tiles:
        if tile_suit(x) != t:
            return 0
        num.append(tile_num(x))
    if num.count(1) < 3 or num.count(9) < 3:
        return 0
    for i in range(2, 9):
        if num.count(i) < 1:
            return 0
    return 26 if gtac.ting_count == 9 else 0


@high_level_yaku(chun_zheng_jiu_lian_bao_deng)
@men_qing_only
def jiu_lian_bao_deng(gtac: TilesAndCond) -> int:
    t = tile_suit(gtac.all_tiles[0])
    num = []
    for x in gtac.all_tiles:
        if tile_suit(x) != t:
            return 0
        num.append(tile_num(x))
    if num.count(1) < 3 or num.count(9) < 3:
        return 0
    for i in range(2, 9):
        if num.count(i) < 1:
            return 0
    return 26


def tian_hu(gtac: TilesAndCond) -> int:
    if gtac.is_qin and gtac.is_tian_hu:
        return 13
    return 0


def di_hu(gtac: TilesAndCond) -> int:
    if gtac.is_zi and gtac.is_di_hu:
        return 13
    return 0
