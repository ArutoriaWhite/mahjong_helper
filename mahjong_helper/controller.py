import os
from copy import deepcopy
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

from tile import TilesAndCond, TileGroup, TILES, TILSE2id
from view import View
import yaku
import points

CH2EN = {'東':'east', '西':'west', '南':'south', '北':'north'}

class Controller:

    def __init__(self):
        self.tac: TilesAndCond = TilesAndCond()
        self.view: View = View(self)

        self.tile_handler = []
        for t in TILES:
            def handler_fac(pt):
                def handler():      # add a group if any call-tile-mode is on, else add free tile)
                    # print(self.tac.group_tiles)
                    # print(self.tac.free_tiles)                    
                    mode = self.view.tile_inp_mode.get()
                    need_update_display = 0

                    if not self.tac.is_full:
                        if mode == 0:       
                            self.tac.free_tiles.append(pt)
                            need_update_display = 1          
                    
                    if 14 - len(self.tac.group_tiles)*3 - len(self.tac.free_tiles) >= 3:
                        if mode == 1:   # chi
                            if yaku.tile_suit != 'honors' and int(yaku.tile_num(pt))<=7:
                                t2 = f'{yaku.tile_suit(pt)}-{int(yaku.tile_num(pt))+1}'
                                t3 = f'{yaku.tile_suit(pt)}-{int(yaku.tile_num(pt))+2}'
                                self.tac.group_tiles.append(TileGroup([pt,t2,t3],1))
                        if mode == 2:   # pong
                            self.tac.group_tiles.append(TileGroup([pt,pt,pt],1))
                        if mode == 3:   # gang
                            self.tac.group_tiles.append(TileGroup([pt,pt,pt,pt],1))
                        if mode == 4:
                            self.tac.group_tiles.append(TileGroup([pt,pt,pt,pt],0))
                        need_update_display = 1
                    
                    if need_update_display:
                        self.update_tile_display()

                return handler
            self.tile_handler.append(handler_fac(t))

    def calc_handler(self):     # pass a, start calculating
        lack = 14-len(self.tac.group_tiles)*3-len(self.tac.free_tiles)
        if lack > 1: return

        self.tac.last_tile = self.tac.free_tiles[-1]
        self.tac.is_tsumo = self.view.is_tsumo.get()
        self.tac.is_double_riichi = self.view.is_double_riichi.get()
        self.tac.is_riichi = self.view.is_riichi.get()
        self.tac.chang_fong = CH2EN[self.view.chang_fong.get()]
        self.tac.zi_fong = CH2EN[self.view.zi_fong.get()]
        self.tac.doras = self.view.doras.get()
        self.tac.is_ippatsu = self.view.is_ippatsu.get()
        self.tac.is_chiang_gang = self.view.is_chiang_gang.get()
        self.tac.is_ling_shang_kai_hua = self.view.is_ling_shang_kai_hua.get()
        self.tac.is_he_di_lao_yu = self.view.is_he_di_lao_yu.get()
        self.tac.is_hai_di_lao_yue = self.view.is_hai_de_lao_yue.get()
        self.tac.is_tian_hu = self.view.is_tian_hu.get()
        self.tac.is_di_hu = self.view.is_di_hu.get()

        if lack == 0:
            self.view.display_result(points.highest_point(self.tac))
        if lack == 1:
            res, last_tile =  points.highest_ting_points(self.tac)
            if res.basic > 0:
                self.view.display_result(res)
                tid = TILSE2id[last_tile]
                self.view.display_single_tile(tid, self.tile_handler[tid], 17, ttk.INFO)
                self.tac.free_tiles.append(last_tile)

    def upload_handler(self):
        pass

    def update_tile_display(self):
        pass
        def ghandler_fac(j):
            def handler():
                self.tac.group_tiles.pop(j)
                self.update_tile_display()
            return handler

        def shandler_fac(j):
            def handler():
                self.tac.free_tiles.pop(j)
                self.update_tile_display()
            return handler

        self.view.clear_display()
        for i,g in enumerate(self.tac.group_tiles):
            tile_id = [TILSE2id[t] for t in g.tiles]
            self.view.display_group_tile(tile_id, ghandler_fac(i))
        for i,t in enumerate(self.tac.free_tiles):
            self.view.display_single_tile(TILSE2id[t], shandler_fac(i))


    def runApp(self):
        self.view.setup_ui()
        self.view.root.mainloop()

    # 所有按鈕會對應到特定的牌 or group
    # 所有按鈕會有對應到 tile id or group id
    # 所有按鈕會需要知道他是 tile 或 group
    # 當按下按鈕：發送 command，執行含有 id 的
    # 當刪除一個之後
    # 1. 全部重新渲染（移除按鈕們, 從陣列裡移除，重新製造按鈕們）
    # 2. 把後面的重新渲染

if __name__ == '__main__':
    ctrl = Controller()
    ctrl.runApp()