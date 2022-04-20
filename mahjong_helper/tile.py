import collections
from email.policy import default
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
        self.free_tiles: list[str] = []
        self.group_tiles: list[TileGroup]  = []     #eye in last
        self.ting_count: int = 0
        self.is_tsumo: bool = False
        self.chang_fong: str = ''
        self.zi_fong: str = ''      # 'west'
        self.doras: collections.defaultdict[str,int] = collections.defaultdict(int)      #which dora, count
        self.is_riichi: bool = False
        self.is_double_riichi: bool = False
        self.is_ippatsu: bool = False
        self.is_chiang_gang: bool = False
        self.is_ling_shang_kai_hua: bool = False
        self.is_hai_di_lao_yue: bool = False
        self.is_he_di_lao_yu: bool = False
        self.is_tian_hu: bool = False
        self.is_di_hu: bool = False
        self.is_qin: bool = False
        self.free_ting: int = 0
        self.group_ting: int = 0

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