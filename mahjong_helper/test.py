from platform import java_ver
import yaku
from tile import TilesAndCond
from tile import TileGroup
import collections


def yaku_test():
    gtac = TilesAndCond()
    gtac.group_tiles = [
        TileGroup([], 0),
        TileGroup([], 0),
        TileGroup([], 0),
        TileGroup([], 0),
        TileGroup([], 0)
    ]
    gtac.free_tiles = []
    gtac.ting_count = 9
    gtac.chang_fong = 'east'
    gtac.zi_fong = 'east'
    gtac.doras = collections.defaultdict(int)

    print(yaku.dora(gtac))
    print(yaku.chang_feng_pai(gtac))
    print(yaku.zi_feng_pai(gtac))
    print(yaku.san_yuan_pai(gtac))
    print(yaku.duan_yao_jiu(gtac))
    print(yaku.ping_he(gtac))
    print(yaku.yi_bei_kou(gtac))
    print(yaku.xiao_san_yuan(gtac))
    print(yaku.san_gang_zi(gtac))
    print(yaku.hun_lao_tou(gtac))
    print(yaku.san_an_ke(gtac))
    print(yaku.hun_yi_se(gtac))
    print(yaku.dui_dui_he(gtac))
    print(yaku.san_se_tong_ke(gtac))
    print(yaku.san_se_tong_shun(gtac))
    print(yaku.hun_quan_dai_yao_jiu(gtac))
    print(yaku.yi_qi_tong_guan(gtac))
    print(yaku.hun_yi_se(gtac))
    print(yaku.chun_quan_dai_yao_jiu(gtac))
    print(yaku.er_bei_kou(gtac))
    print(yaku.qing_yi_se(gtac))
    print(yaku.da_si_xi(gtac))
    print(yaku.si_an_ke_dan_ji(gtac))
    print(yaku.chun_zheng_jiu_lian_bao_deng(gtac))
    print(yaku.da_san_yuan(gtac))
    print(yaku.si_gang_zi(gtac))
    print(yaku.qing_lao_tou(gtac))
    print(yaku.xiao_si_xi(gtac))
    print(yaku.zi_yi_se(gtac))
    print(yaku.lv_yi_se(gtac))
    print(yaku.si_an_ke(gtac))


yaku_test()
