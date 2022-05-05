import imp
import os
from copy import deepcopy
from pdb import lasti2lineno
from sys import displayhook
import tkinter as tk
from tkinter import messagebox
from typing import Callable
from numpy import tile
import ttkbootstrap as ttk
from PIL import Image, ImageTk

#from controller import TILES, Controller
from tile import TilesAndCond, TILES, TILSE2id
from points import RonResult
from yaku import yaku_name2id

yaku_names_CH = [
    '寶牌','斷么九','搶槓',
    '嶺上開花','海底摸月','河底撈魚',
    '一發','門清自摸','平和',
    '場風牌','自風牌','三元牌',
    '小三元','三槓子','混老頭',
    '三暗刻','對對和','三色同刻',
    '三色同順','一氣通貫','雙立直',
    '立直','七對子','純全帶么久',
    '混全帶么九','二盃口','一盃口',
    '清一色','混一色','大四喜',
    '小四喜','大三元','四槓子',
    '清老頭','字一色','綠一色',
    '四暗刻單騎','四暗刻','國士無雙十三面',
    '國士無雙','純正九蓮寶燈','九蓮寶燈',
    '天和','地和'
]

class View:

    def __init__(self, _controller):
        self.ctrl = _controller
    
    def setup_ui(self):

        # assets
        self.absFilePath = os.path.split(os.path.abspath(__file__))[0]
        #tile_imgs = [tk.PhotoImage(file=os.path.join(absFilePath,f'img/tiles/{t}.png')) for t in tiles]
        self.tile_imgs = [Image.open(os.path.join(self.absFilePath,f'img/tiles/{t}.png')) for t in TILES]


        # root configure
        self.style = ttk.Style(theme='lumen')
        self.root: tk.Tk = self.style.master
        self.width, self.height = 1200, 800
        self.scr_width, self.scr_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f'{self.width}x{self.height}+{(self.scr_width-self.width)//2}+{(self.scr_height-self.height)//2}')
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=3)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=2)

        # main frames configure
        pad = 10
        self.frm_display = ttk.LabelFrame(self.root, text='手牌（最後一張為榮和／自摸的牌）', bootstyle=ttk.INFO)   # type: ignore
        self.frm_display.grid(column=0, row=0, columnspan=2,padx=2*pad, pady=2*pad, ipadx=pad, ipady=pad, sticky='nswe')
        self.frm_tile = ttk.Labelframe(self.root, text='手牌輸入')
        self.frm_tile.grid(column=0, row=1, padx=2*pad, pady=2*pad, ipadx=pad, ipady=pad, sticky='nswe')
        self.frm_cbx = ttk.LabelFrame(self.root, text='附加')
        self.frm_cbx.grid(column=0, row=2, padx=2*pad, pady=2*pad, ipadx=pad, ipady=pad, sticky='nswe')
        self.frm_res = ttk.LabelFrame(self.root, text='結果')
        self.frm_res.grid(column=1, row=1, rowspan=3, padx=2*pad, pady=2*pad, ipadx=pad, ipady=pad,sticky='nswe')


        # in frm_tile
        self.frm_tile.columnconfigure(0, weight=1)
        self.frm_tile.columnconfigure(1, weight=9)
        self.frm_tile.rowconfigure(0, weight=4)
        self.frm_tile.rowconfigure(1, weight=1)
        self.frm_call = ttk.Frame(self.frm_tile)
        self.frm_call.grid(column=0, row=0, padx=pad, pady=pad, sticky='nswe')
        self.frm_all_tile = ttk.LabelFrame(self.frm_tile, text='所有牌')
        self.frm_all_tile.grid(column=1, row=0, padx=pad, pady=pad, sticky='nswe')

        # call buttons
        self.frm_call.columnconfigure(0, weight=1)
        self.frm_call.rowconfigure([0, 1, 2, 3], weight=1)  # type: ignore
        self.tile_inp_mode = ttk.IntVar()    # 0: hand, 1: chi, 2: pung, 3: gang, 4: an gang
        ttk.Radiobutton(self.frm_call, text='手牌', bootstyle=(ttk.INFO,ttk.TOOLBUTTON), variable=self.tile_inp_mode, value=0).grid(column=0, row=0, padx=pad, pady=pad)  # type: ignore
        ttk.Radiobutton(self.frm_call, text='吃', bootstyle=(ttk.INFO,ttk.TOOLBUTTON), variable=self.tile_inp_mode, value=1).grid(column=0, row=1, padx=pad, pady=pad)  # type: ignore
        ttk.Radiobutton(self.frm_call, text='碰', bootstyle=(ttk.INFO,ttk.TOOLBUTTON), variable=self.tile_inp_mode, value=2).grid(column=0, row=2, padx=pad, pady=pad)  # type: ignore
        ttk.Radiobutton(self.frm_call, text='槓', bootstyle=(ttk.INFO,ttk.TOOLBUTTON), variable=self.tile_inp_mode, value=3).grid(column=0, row=3, padx=pad, pady=pad)  # type: ignore
        ttk.Radiobutton(self.frm_call, text='暗槓', bootstyle=(ttk.INFO,ttk.TOOLBUTTON), variable=self.tile_inp_mode, value=4).grid(column=0, row=4, padx=pad, pady=pad)  # type: ignore
        ttk.Label(self.frm_tile, text='或').grid(column=0, row=1, padx=pad, sticky='e')
        ttk.Button(self.frm_tile, text='上傳圖片', command=self.ctrl.upload_handler).grid(column=1, row=1, padx=pad, pady=pad, sticky='w')

        # doras
        self.frm_dora = ttk.Frame(self.frm_tile)
        self.frm_dora.columnconfigure((0,1,2), weight=1) # type: ignore
        self.frm_dora.grid(column=1, row=1, padx=pad, pady=pad)
        ttk.Label(self.frm_dora, text='寶牌: ').grid(column=0, row=0, padx=pad)
        self.doras = ttk.IntVar()
        ttk.Spinbox(self.frm_dora, from_=0, to=999, increment=1, textvariable=self.doras, width=2).grid(column=1, row=0)

        # all tile
        self.frm_all_tile.columnconfigure(list(range(9)), weight=1)  # type: ignore
        self.frm_all_tile.rowconfigure(list(range(4)), weight=1)  # type: ignore
        self.tile_btn_img = [ImageTk.PhotoImage(i) for i in self.tile_imgs]
        for i,t in enumerate(TILES):
            ttk.Button(self.frm_all_tile, image=self.tile_btn_img[i], width=2, bootstyle=(ttk.SECONDARY,ttk.OUTLINE), command=self.ctrl.tile_handler[i]).grid(column=i%9,row=i//9)  # type: ignore


        # in frm_cbx
        self.is_tsumo =  ttk.BooleanVar()
        self.is_riichi = ttk.BooleanVar()
        self.is_double_riichi = ttk.BooleanVar()
        self.is_ippatsu = ttk.BooleanVar()
        self.chang_fong = ttk.StringVar()
        self.zi_fong = ttk.StringVar()
        self.is_chiang_gang = ttk.BooleanVar()
        self.is_ling_shang_kai_hua = ttk.BooleanVar()
        self.is_hai_de_lao_yue = ttk.BooleanVar()
        self.is_he_di_lao_yu = ttk.BooleanVar()
        self.is_tian_hu = ttk.BooleanVar()
        self.is_di_hu = ttk.BooleanVar()

        self.frm_cbx.columnconfigure(list(range(10)), weight=1) # type: ignore
        self.frm_cbx.rowconfigure(list(range(4)), weight=1) # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='自摸', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_tsumo).grid(row=0, column=0, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='立直', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_riichi).grid(row=1, column=0, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='雙立直', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_double_riichi).grid(row=2, column=0, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='一發', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_ippatsu).grid(row=3, column=0, columnspan=2)  # type: ignore
        ttk.Label(self.frm_cbx, text='場風: ', padding=pad).grid(row=0, column=2, sticky='e')
        ttk.OptionMenu(self.frm_cbx, self.chang_fong, '東', '東', '南', '西', '北').grid(row=0, column=3, sticky='w')
        ttk.Label(self.frm_cbx, text='自風: ', padding=pad).grid(row=1, column=2, sticky='e')
        ttk.OptionMenu(self.frm_cbx, self.zi_fong, '東', '東', '南', '西', '北').grid(row=1, column=3, sticky='w')
        ttk.Checkbutton(self.frm_cbx, text='搶槓', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_chiang_gang).grid(row=0, column=4, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='嶺上開花', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_ling_shang_kai_hua).grid(row=1, column=4, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='海底摸月', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_hai_de_lao_yue).grid(row=2, column=4, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='河底撈魚', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_he_di_lao_yu).grid(row=3, column=4, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='天和', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_tian_hu).grid(row=0, column=6, columnspan=2)  # type: ignore
        ttk.Checkbutton(self.frm_cbx, text='地和', padding=pad, bootstyle=(ttk.SQUARE,ttk.TOGGLE), variable=self.is_di_hu).grid(row=1, column=6, columnspan=2)  # type: ignore


        # preview in frm_res
        self.frm_res.columnconfigure((0,1), weight=1) # type: ignore
        self.frm_res.rowconfigure(list(range(20)), weight=1) # type: ignore
        #ttk.Label(self.frm_res, text='四暗刻單騎').grid(row=0,column=0)
        #ttk.Label(self.frm_res, text='13飜').grid(row=0,column=1)
        ttk.Label(self.frm_res, text='排版用文字排版用文字排版', foreground='white').grid(row=1,column=0)
        ttk.Label(self.frm_res, text='排版用文字排版用文字排版', foreground='white').grid(row=1,column=1)
        ttk.Separator(self.frm_res).grid(row=14,column=0,columnspan=2,sticky='nwe')
        # ttk.Label(self.frm_res, text='40符').grid(row=14,column=0)
        # ttk.Label(self.frm_res, text='26飜').grid(row=14,column=1)
        # ttk.Label(self.frm_res, text='雙倍役滿', font=('Times', 20, 'bold italic')).grid(row=15,column=0,rowspan=2)
        # ttk.Label(self.frm_res, text='24000 / 48000 點', font=('Times', 20, 'bold italic')).grid(row=15,column=1,rowspan=2)
        ttk.Separator(self.frm_res).grid(row=17,column=0,columnspan=2,sticky='we')
        ttk.Button(self.frm_res, text='計算', bootstyle=(ttk.SUCCESS), command=self.ctrl.calc_handler).grid(row=18,column=0,columnspan=2)  # type: ignore
        self.res_wid = []

        # for show tiles
        self.frm_display.columnconfigure(list(range(18)), weight=1) # type: ignore
        self.frm_display.rowconfigure(0, weight=1)
        self.show_tile_img = [ImageTk.PhotoImage(t.resize((36,42))) for t in self.tile_imgs]
        ttk.Button(self.frm_display, image=self.show_tile_img[-3], bootstyle=(ttk.LINK)).grid(row=0, column=0) # type: ignore
        self.cnt = 0
        self.now_display_tiles: list[ttk.Button|ttk.Frame] = []

    def clear_display(self):
        self.cnt = 0
        for i in range(len(self.now_display_tiles)-1, -1, -1):
            self.now_display_tiles[i].destroy()

    def display_single_tile(self, tile_id: int, handler: Callable, col: int=-1, style = ttk.SECONDARY):
        self.now_display_tiles.append(ttk.Button(self.frm_display, image=self.show_tile_img[tile_id], bootstyle=(style,ttk.OUTLINE), command=handler, width=3))     # type: ignore
        self.now_display_tiles[-1].grid(row=0, column=col if col>=0 else self.cnt)
        self.cnt += 1

    def display_group_tile(self, tile_id: list[int], handler: Callable):
        frm_group = ttk.Frame(self.frm_display)
        frm_group.grid(row=0, column=self.cnt, columnspan=len(tile_id))
        self.now_display_tiles.append(frm_group)
        for i,t in enumerate(tile_id):
            ttk.Button(frm_group, image=self.show_tile_img[t], bootstyle=(ttk.SECONDARY,ttk.OUTLINE), command=handler).grid(row=0, column=i)  # type: ignore
        self.cnt += 4

    def point_name(self, basic) -> str:
        if basic < 2000:
            return ''
        if basic < 3000:
            return '滿貫'
        if basic < 4000:
            return '跳滿'
        if basic < 6000:
            return '倍滿'
        if basic < 8000:
            return '三倍滿'
        if basic < 16000:
            return '役滿'
        ch_num = ['兩','三','四','五','六','七','八','九','十']
        return f'{ch_num[(basic//8000)-2]}倍役滿'

    def display_result(self, res: RonResult):
        for w in self.res_wid:
            w.destroy()
        res.yakus.sort(reverse=True)
        for i,y in enumerate(res.yakus):

            yname = yaku_names_CH[yaku_name2id[y[1]]]
            self.res_wid.append(ttk.Label(self.frm_res, text=yname))
            self.res_wid[-1].grid(row=i,column=0)
            self.res_wid.append(ttk.Label(self.frm_res, text=f'{y[0]} 飜'))
            self.res_wid[-1].grid(row=i,column=1)

            self.res_wid.append(ttk.Label(self.frm_res, text=f'{res.fu} 符'))
            self.res_wid[-1].grid(row=14,column=0)
            self.res_wid.append(ttk.Label(self.frm_res, text=f'{res.fan} 飜'))
            self.res_wid[-1].grid(row=14,column=1)
            self.res_wid.append(ttk.Label(self.frm_res, text=f'{self.point_name(res.basic)}', font=('Times', 20, 'bold italic')))
            self.res_wid[-1].grid(row=15,column=0,rowspan=2)
            self.res_wid.append(ttk.Label(self.frm_res, text=f'{res.tsumo} / {res.ron} 點', font=('Times', 20, 'bold italic')))
            self.res_wid[-1].grid(row=15,column=1,rowspan=2)        
        

# Controller set handler for view
# 1. bind in controller
# 2. controller assgined handler to view.py
# 3. assign controller instance to view.py