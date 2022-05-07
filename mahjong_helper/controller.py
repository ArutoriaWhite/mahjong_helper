import os
import tkinter as tk
from copy import deepcopy
from typing import Callable

import ttkbootstrap as ttk
from PIL import Image, ImageTk

import points
import yaku
from tile import *
from view import View


CH2EN = {'東': 'east', '西': 'west', '南': 'south', '北': 'north'}


class Controller:

    def __init__(self):
        self.tac: TilesAndCond = TilesAndCond()
        self.view: View = View(self)

        self.add_tile_btn_handler: list[Callable] = []
        for tile_of_btn in TILES:
            def handler_fac(t):
                def handler():      # add a group if any call-tile-mode is on, else add free tile)
                    mode = self.view.add_tile_mode.get()
                    need_update_display = 0

                    if self.tac.lack >= 0:
                        if mode == 0:
                            self.tac.free_tiles.append(t)
                            need_update_display = 1
                    if self.tac.lack >= 3:
                        if mode == 1:   # chi
                            if yaku.tile_suit != HONORS and int(yaku.tile_num(t)) <= 7:
                                t2 = f'{yaku.tile_suit(t)}-{int(yaku.tile_num(t))+1}'
                                t3 = f'{yaku.tile_suit(t)}-{int(yaku.tile_num(t))+2}'
                                self.tac.group_tiles.append(TileGroup([t, t2, t3], 1))
                        if mode == 2:   # pong
                            self.tac.group_tiles.append(TileGroup([t, t, t], 1))
                        if mode == 3:   # gang
                            self.tac.group_tiles.append(TileGroup([t, t, t, t], 1))
                        if mode == 4:
                            self.tac.group_tiles.append(TileGroup([t, t, t, t], 0))
                        need_update_display = 1
                    if need_update_display:
                        self.update_tile_display()
                    pass

                return handler

            self.add_tile_btn_handler.append(handler_fac(tile_of_btn))

    def calc_btn_handler(self):
        self.view.clear_result_display()
        if self.tac.lack > 1:
            return

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

        if self.tac.lack == 0:
            self.view.display_result(points.highest_point(self.tac))
        if self.tac.lack == 1:
            res, last_tile = points.find_last_tile(self.tac)
            if res.basic > 0:
                self.view.display_result(res)
                tid = TILSE2ID[last_tile]
                self.view.display_single_tile(
                    tid, self.add_tile_btn_handler[tid], 17, ttk.INFO)
                self.tac.free_tiles.append(last_tile)

    def upload_img_btn_handler(self):   # this functions is not implemented
        pass

    def update_tile_display(self):
        def group_handler_fac(j):
            def handler():
                self.tac.group_tiles.pop(j)
                self.update_tile_display()
            return handler

        def single_handler_fac(j):
            def handler():
                self.tac.free_tiles.pop(j)
                self.update_tile_display()
            return handler

        self.view.clear_tile_display()
        for i, g in enumerate(self.tac.group_tiles):
            tile_id = [TILSE2ID[t] for t in g.tiles]
            self.view.display_group_tile(tile_id, group_handler_fac(i))
        for i, t in enumerate(self.tac.free_tiles):
            self.view.display_single_tile(TILSE2ID[t], single_handler_fac(i))

    def runApp(self):
        self.view.setup_ui()
        self.view.root.mainloop()


if __name__ == '__main__':
    ctrl = Controller()
    ctrl.runApp()
