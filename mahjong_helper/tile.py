import collections

from .utils import eprint


HONORS = 'honors'
GREEN = 'green'
RED = 'red'
WHITE = 'white'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'
NORTH = 'north'
BAMBOO = 'b'
CHARACTERS = 'c'
DOTS = 'd'


TILES =  [f'{CHARACTERS}-{i}' for i in range(1, 10)]\
        +[f'{DOTS}-{i}' for i in range(1, 10)]\
        +[f'{BAMBOO}-{i}' for i in range(1, 10)]\
        +[f'{HONORS}-{i}' for i in [EAST,SOUTH,WEST,NORTH,WHITE,GREEN,RED]]

TILSE2ID = {}
for i,t in enumerate(TILES):
    TILSE2ID[t] = i


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
        self.last_tile: str = ''
        self.is_tsumo: bool = False
        self.is_double_riichi: bool = False
        self.is_riichi: bool = False
        self.chang_fong: str = ''
        self.zi_fong: str = ''      # 'west'
        #self.doras: collections.defaultdict[str,int] = collections.defaultdict(int)      #which dora, count
        #self.aka_doras: list[str] = []
        self.doras: int = 0
        self.is_ippatsu: bool = False
        self.is_chiang_gang: bool = False
        self.is_ling_shang_kai_hua: bool = False
        self.is_hai_di_lao_yue: bool = False
        self.is_he_di_lao_yu: bool = False
        self.is_tian_hu: bool = False
        self.is_di_hu: bool = False
        
        self.free_ting: int = 0
        self.ting_cnt: int = 0

    @property
    def is_qin(self) -> bool:
        return self.zi_fong == EAST

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
    
    @property
    def unfull_tiles(self) -> list[str]:
        res = self.all_tiles[:]
        res.remove(self.last_tile)
        return res

    @property
    def is_full(self) -> bool:
        return len(self.group_tiles)*3 + len(self.free_tiles) >= 14

    @property
    def lack(self) -> int:
        # kan is count as 3 tiles
        return 14 - len(self.group_tiles)*3 - len(self.free_tiles)

    def _print_content(self):    # for debugging
        eprint("\n===TAC Content===")
        eprint(self.free_tiles)
        for x in self.group_tiles:
            eprint(x)
        eprint(f"group_ting: {self.ting_cnt}")
