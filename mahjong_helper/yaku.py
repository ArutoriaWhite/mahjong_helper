from collections import defaultdict
from posixpath import split
from typing import Optional
from tile import TilesAndCond
from tile import TileGroup

HONORS = 'honors'

############## decorators #################


def men_qing_only(func):
    def wrapper(gtac: TilesAndCond):
        if gtac.is_men_qing:
            return func(gtac)
        return 0
    return wrapper


def fu_lou_minus_one(func):
    def wrapper(gtac: TilesAndCond):
        return func(gtac)-(0 if gtac.is_men_qing else 1)
    return wrapper


def high_level_yaku(higher_yaku):
    def deco(func):
        def wrapper(gtac: TilesAndCond):
            return 0 if higher_yaku(gtac)>0 else func(gtac)
        return wrapper
    return deco

############### helper function ################


def _tile_suit(tile: str) -> str:
    return tile.split('-')[0]


def _tile_num(tile: str) -> int | str:
    if _tile_suit(tile) == HONORS:
        return tile.split('-')[1]
    return int(tile.split('-')[1])


def _is_zi_pai(tile: str) -> bool:
    return _tile_suit(tile) == HONORS


def _is_lao_tou_pai(tile: str) -> bool:
    return _tile_num(tile) == 1 or _tile_num(tile) == 9


def _is_yao_jiu_pai(tile: str) -> bool:
    return _is_zi_pai(tile) or _is_lao_tou_pai(tile)


def _is_san_yuan_pai(tile: str) -> bool:
    s = {'green', 'red', 'white'}
    return _tile_num(tile) in s


def _is_feng_pai(tile: str) -> bool:
    s = {'east', 'south', 'west', 'north'}
    return _tile_num(tile) in s


def _group_type(tiles: list[str]) -> int:
    """
    return
        0: shun
        1: ke
        2: gang
        3: eye
        -1: not either
    """
    tiles = ['-'.join(t.split('-')[0:2]) for t in tiles]
    if [_tile_suit(t) for t in tiles].count(_tile_suit(tiles[0])) != len(tiles):      #all type must be same
        return -1
    if _tile_suit(tiles[0]) != HONORS and len(tiles) == 3:
        nums = sorted([int(_tile_num(t)) for t in tiles])
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


def dora(gtac: TilesAndCond) -> int:
    """Return sum of every type of dora"""
    sum = 0
    for t in gtac.all_tiles:
        sum += gtac.doras[f'{_tile_suit(t)}-{_tile_num(t)}']
        sum += (t[-1] == 'r')
    return sum


def duan_yao_jiu(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if _is_yao_jiu_pai(t):
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
    for g in gtac.group_tiles[:-1]:
        if _group_type(g.tiles) != 0:
            return 0
    yi_pai = {
        gtac.chang_fong,
        gtac.zi_fong,
        'red', 'white', 'green'
    }
    if _tile_num(gtac.eye[0]) not in yi_pai and gtac.ting_count == 2:
        return 1
    return 0


def chang_feng_pai(gtac: TilesAndCond) -> int:
    for g in gtac.group_tiles:
        if _group_type(g.tiles) in {1, 2} and _tile_num(g.tiles[0]) == gtac.chang_fong:
            return 1
    return 0


def zi_feng_pai(gtac: TilesAndCond) -> int:
    for g in gtac.group_tiles:
        if _group_type(g.tiles) in {1, 2} and _tile_num(g.tiles[0]) == gtac.zi_fong:
            return 1
    return 0


def san_yuan_pai(gtac: TilesAndCond) -> int:
    sum = 0
    for g in gtac.group_tiles:
        if _group_type(g.tiles) in {1, 2} and _is_san_yuan_pai(g.tiles[0]):
            sum += 1
    return sum


def xiao_san_yuan(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    eye_cnt = 0
    for g in gtac.group_tiles:
        if _group_type(g.tiles) in {1, 2} and _is_san_yuan_pai(g.tiles[0]):
            ke_cnt += 1
        if _group_type(g.tiles)==3 and _is_san_yuan_pai(g.tiles[0]):
            eye_cnt += 1

    return 2 if ke_cnt == 2 and eye_cnt == 1 else 0


def san_gang_zi(gtac: TilesAndCond) -> int:
    cnt = 0
    for g in gtac.group_tiles:
        if _group_type(g.tiles) == 2:
            cnt += 1
    return (cnt == 3)*2


def hun_lao_tou(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not _is_yao_jiu_pai(t):
            return 0
    return 2


def san_an_ke(gtac: TilesAndCond) -> int:
    cnt = 0
    for g, fl in gtac.group_tiles:
        if (not fl) and _group_type(g) in {1, 2}:
            cnt += 1
    return 2 if cnt == 3 else 0


def dui_dui_he(gtac: TilesAndCond) -> int:
    cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2}:
            cnt += 1
    return 2 if cnt == 4 else 0


def san_se_tong_ke(gtac: TilesAndCond) -> int:
    num_cnt = defaultdict(int)
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and _tile_suit(g[0]) != HONORS:
            num_cnt[_tile_num(g[0])] += 1
    for k, v in num_cnt.items():
        if v >= 3:
            return 3
    return 0


@fu_lou_minus_one
def san_se_tong_shun(gtac: TilesAndCond) -> int:
    types = defaultdict(set)
    for g, fl in gtac.group_tiles:
        if _group_type(g) == 0 and _tile_suit(g[0]) != HONORS:
            types[_tile_num(g[0])].add(_tile_suit(g[0]))
    for k, v in types.items():
        if len(v)>=3:
            return 3
    return 0


@fu_lou_minus_one
def yi_qi_tong_guan(gtac: TilesAndCond) -> int:
    shun = defaultdict(set)
    for g, fl in gtac.group_tiles:
        if _group_type(g) == 0 and _tile_suit(g[0]) != HONORS:
            shun[_tile_suit(g[0])].add(_tile_num(g[0]))
    for k, v in shun.items():
        if {1, 4, 7}.issubset(v):
            return 3
    return 0


@men_qing_only
def double_riichi(gtac: TilesAndCond) -> int:
    return gtac.is_double_riichi*2


@high_level_yaku(double_riichi)
@men_qing_only
def riichi(gtac: TilesAndCond) -> int:
    return gtac.is_riichi*1


@men_qing_only
def qi_dui_zi(gtac: TilesAndCond) -> int:
    return 2 if len(gtac.group_tiles) == 7 else 0


@fu_lou_minus_one
def chun_quan_dai_yao_jiu(gtac: TilesAndCond) -> int:
    shun_cnt = 0
    ke_cnt = 0
    eye_cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and _is_lao_tou_pai(g[0]):
            ke_cnt += 1
        if _group_type(g) == 0:
            if _is_lao_tou_pai(g[0]) or _is_lao_tou_pai(g[-1]):
                shun_cnt += 1
        if _group_type(g) == 3 and _is_lao_tou_pai(g[0]):
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
        if _group_type(g) in {1, 2} and _is_yao_jiu_pai(g[0]):
            ke_cnt += 1
        if _group_type(g) == 0:
            if _is_lao_tou_pai(g[0]) or _is_lao_tou_pai(g[-1]):
                shun_cnt += 1
        if _group_type(g) == 3 and _is_yao_jiu_pai(g[0]):
            eye_cnt += 1
    if (shun_cnt+ke_cnt) == 4 and shun_cnt > 0 and eye_cnt > 0:
        return 3
    return 0


@men_qing_only
def er_bei_kou(gtac: TilesAndCond) -> int:
    tile_cnt = defaultdict(int)
    for g, fl in gtac.group_tiles:
        if _group_type(g) == 0:
            tile_cnt[g[0]] += 1
    yi_bei_kou_cnt = 0
    for k, v in tile_cnt.items():
        if v >= 2:
            yi_bei_kou_cnt += 1
    if yi_bei_kou_cnt >= 2:
        return 3
    return 0


@high_level_yaku(er_bei_kou)
@men_qing_only
def yi_bei_kou(gtac: TilesAndCond) -> int:
    tile_cnt = defaultdict(int)
    for g, fl in gtac.group_tiles:
        if _group_type(g) == 0:
            tile_cnt[g[0]] += 1
    yi_bei_kou_cnt = 0
    for k, v in tile_cnt.items():
        if v >= 2:
            yi_bei_kou_cnt += 1
    if yi_bei_kou_cnt >= 1:
        return 1
    return 0


@fu_lou_minus_one
def qing_yi_se(gtac: TilesAndCond) -> int:
    t = _tile_suit(gtac.all_tiles[0])
    if t == HONORS:
        return 0
    for g, fl in gtac.group_tiles:
        if _tile_suit(g[0]) != t:
            return 0
    return 6


@high_level_yaku(qing_yi_se)
@fu_lou_minus_one
def hun_yi_se(gtac: TilesAndCond) -> int:
    t = None
    for g, fl in gtac.group_tiles:
        if _tile_suit(g[0]) == HONORS:
            continue
        if t:
            if _tile_suit(g[0]) != t:
                return 0
        else:
            t = _tile_suit(g[0])
    return 3


def da_si_xi(gtac: TilesAndCond) -> int:
    feng = set()
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and _is_feng_pai(g[0]):
            feng.add(g[0])
    if len(feng) == 4:
        return 26
    return 0

@high_level_yaku(da_si_xi)
def xiao_si_xi(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    eye_cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and _is_feng_pai(g[0]):
            ke_cnt += 1
        if _group_type(g) == 3 and _is_feng_pai(g[0]):
            eye_cnt += 1
    return 13 if ke_cnt == 3 and eye_cnt == 1 else 0


def da_san_yuan(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and _is_san_yuan_pai(g[0]):
            ke_cnt += 1
    return 13 if ke_cnt >= 3 else 0


def si_gang_zi(gtac: TilesAndCond) -> int:
    gang_cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) == 2:
            gang_cnt += 1
    return 13 if gang_cnt >= 4 else 0


def qing_lao_tou(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not _is_lao_tou_pai(t):
            return 0
    return 13


def zi_yi_se(gtac: TilesAndCond) -> int:
    for t in gtac.all_tiles:
        if not _is_zi_pai(t):
            return 0
    return 13


def lv_yi_se(gtac: TilesAndCond) -> int:
    s = {2, 3, 4, 6, 8}
    for t in gtac.all_tiles:
        if _tile_suit(t) == HONORS:
            if _tile_num(t) != 'green':
                return 0
        else:
            if _tile_suit(t) != 'bamboo' or _tile_num(t) not in s:
                return 0
    return 13


@men_qing_only
def si_an_ke_dan_ji(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    if gtac.ting_count > 1:
        return 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and (not fl):
            ke_cnt += 1
    return 26 if ke_cnt >= 4 else 0


@high_level_yaku(si_an_ke_dan_ji)
@men_qing_only
def si_an_ke(gtac: TilesAndCond) -> int:
    ke_cnt = 0
    for g, fl in gtac.group_tiles:
        if _group_type(g) in {1, 2} and (not fl):
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
    t = _tile_suit(gtac.all_tiles[0])
    num = []
    for x in gtac.all_tiles:
        if _tile_suit(x) != t:
            return 0
        num.append(_tile_num(x))
    if num.count(1) < 3 or num.count(9) < 3:
        return 0
    for i in range(2, 9):
        if num.count(i) < 1:
            return 0
    return 26 if gtac.ting_count == 9 else 0


@high_level_yaku(chun_zheng_jiu_lian_bao_deng)
@men_qing_only
def jiu_lian_bao_deng(gtac: TilesAndCond) -> int:
    t = _tile_suit(gtac.all_tiles[0])
    num = []
    for x in gtac.all_tiles:
        if _tile_suit(x) != t:
            return 0
        num.append(_tile_num(x))
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

yaku_checkers = [
    dora,duan_yao_jiu,chiang_gang,
    ling_shang_kai_hua,hai_di_lao_yue,he_di_lao_yu,
    ippatsu,men_qing_tsumo,ping_he,
    chang_feng_pai,zi_feng_pai,san_yuan_pai,
    xiao_san_yuan,san_gang_zi,hun_lao_tou,
    san_an_ke,dui_dui_he,san_se_tong_ke,
    san_se_tong_shun,yi_qi_tong_guan,double_riichi,
    riichi,qi_dui_zi,chun_quan_dai_yao_jiu,
    hun_quan_dai_yao_jiu,er_bei_kou,yi_bei_kou,
    qing_yi_se,hun_yi_se,da_si_xi,
    xiao_si_xi,da_san_yuan,si_gang_zi,
    qing_lao_tou,zi_yi_se,lv_yi_se,
    si_an_ke_dan_ji,si_an_ke,guo_shi_wu_shuang_shi_san_mian,
    guo_shi_wu_shuang,chun_zheng_jiu_lian_bao_deng,jiu_lian_bao_deng,
    tian_hu,di_hu
]
yaku_names = [
    'dora','duan_yao_jiu','chiang_gang'
    ,'ling_shang_kai_hua','hai_di_lao_yue','he_di_lao_yu',
    'ippatsu','men_qing_tsumo','ping_he',
    'chang_feng_pai','zi_feng_pai','san_yuan_pai',
    'xiao_san_yuan','san_gang_zi','hun_lao_tou',
    'san_an_ke','dui_dui_he','san_se_tong_ke',
    'san_se_tong_shun','yi_qi_tong_guan','double_riichi'
    ,'riichi','qi_dui_zi','chun_quan_dai_yao_jiu',
    'hun_quan_dai_yao_jiu','er_bei_kou','yi_bei_kou',
    'qing_yi_se','hun_yi_se','da_si_xi',
    'xiao_si_xi','da_san_yuan','si_gang_zi',
    'qing_lao_tou','zi_yi_se','lv_yi_se',
    'si_an_ke_dan_ji','si_an_ke','guo_shi_wu_shuang_shi_san_mian',
    'guo_shi_wu_shuang','chun_zheng_jiu_lian_bao_deng','jiu_lian_bao_deng',
    'tian_hu','di_hu'
]

yaku_name2id = {}
for i,y in enumerate(yaku_names):
    yaku_name2id[y] = i

yakumans = {
    'da_si_xi','xiao_si_xi','da_san_yuan',
    'si_gang_zi','qing_lao_tou','zi_yi_se',
    'lv_yi_se','si_an_ke_dan_ji','si_an_ke',
    'guo_shi_wu_shuang_shi_san_mian','guo_shi_wu_shuang',
    'chun_zheng_jiu_lian_bao_deng','jiu_lian_bao_deng',
    'tian_hu','di_hu'
}

if __name__=='__main__':        # just for test
    import collections
    gtac = TilesAndCond()
    gtac.group_tiles = [
        TileGroup(['dots-1-n','dots-1-n','dots-1-n'], 0),
        TileGroup(['honors-west-n','honors-west-n','honors-west-n'], 0),
        TileGroup(['honors-east-n','honors-east-n','honors-east-n'], 0),
        TileGroup(['honors-south-n','honors-south-n','honors-south-n'], 0),
        TileGroup(['honors-north-n','honors-north-n'], 0)
    ]
    gtac.free_tiles = []
    gtac.ting_count = 9
    gtac.chang_fong = 'east'
    gtac.zi_fong = 'east'
    gtac.doras = collections.defaultdict(int)

    for i,y in enumerate(yaku_checkers):
        if y(gtac) > 0:
            print(f'{yaku_names[i]}: {y(gtac)}')
