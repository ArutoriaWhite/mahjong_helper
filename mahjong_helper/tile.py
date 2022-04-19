import collections
#tiles classes En naming reference to https://github.com/Camerash/mahjong-dataset
#aka dora example: dots-8-r
#normal example: dots-8-n

TileGroup = collections.namedtuple('TileGroup','tiles is_fu_lou')

class TilesAndCond:
    def __init__ (self) -> None:
        """
        grouped_tiles:
            eye in last
            shun is sorted
        """
        self.free_tiles: list[str]
        self.group_tiles: list[TileGroup] #eye in last
        self.ting_count: int
        self.is_tsumo: bool
        self.chang_fong: str
        self.zi_fong: str
        self.doras: collections.defaultdict[str,int] #which dora, count
        self.is_riichi: bool
        self.is_double_riichi: bool
        self.is_ippatsu: bool
        self.is_chiang_gang: bool
        self.is_ling_shang_kai_hua: bool
        self.is_hai_di_lao_yue: bool
        self.is_he_di_lao_yu: bool
        self.is_tian_hu: bool
        self.is_di_hu: bool
        self.is_qin: bool

    @property
    def is_men_qing (self) -> bool:
        for g in self.group_tiles:
            if g[1]: #is fu lou
                return False
        return True

    @property
    def eye(self) -> list[str]:
        return self.group_tiles[-1].tiles
    
    @property
    def is_ron(self) -> bool:
        return not self.is_tsumo

    @property
    def is_zi(self) -> bool:
        return not self.is_qin
    
    @property
    def all_tiles(self) -> list[str]:
        res = self.free_tiles[:]
        for gg in [g.tiles for g in self.group_tiles]:
            res += gg
        return res