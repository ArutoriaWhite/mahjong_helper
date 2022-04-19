yaku_id2name = [ 
    'dora','duan_yao_jiu','chiang_gang',
    'ling_shang_kai_hua','hai_di_lao_yue','he_di_lao_yu',
    'ippatsu','riichi','men_qing_tsumo',
    'ping_he','yi_bei_kou','chang_feng_pai',
    'zi_feng_pai','san_yuan_pai','xiao_san_yuan',
    'san_gang_zi','hun_lao_tou','san_an_ke',
    'dui_dui_he','san_se_tong_ke','san_se_tong_shun',
    'hun_quan_dai_yao_jiu','yi_qi_tong_guan','double_riichi',
    'qi_dui_zi','hun_yi_se','chun_quan_dai_yao_jiu',
    'er_bei_kou','qing_yi_se','da_si_xi',
    'si_an_ke_dan_ji','guo_shi_wu_shuang_shi_san_mian','chun_zheng_jiu_lian_bao_deng',
    'da_san_yuan','si_gang_zi','qing_lao_tou',
    'xiao_si_xi','zi_yi_se','lv_yi_se',
    'si_an_ke','guo_shi_wu_shuang','jiu_lian_bao_deng',
    'tian_hu','di_hu'
]
yaku_name2id = dict()

#init
for (n,i) in enumerate(yaku_id2name):
    yaku_name2id[n] = i