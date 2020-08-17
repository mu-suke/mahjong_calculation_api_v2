# If you run it, execute this command => "uvicorn main:app --reload"

# FastAPI
from fastapi import FastAPI
# Pydantic
from pydantic import BaseModel
from typing import Optional, List


class Item(BaseModel):
    man_tile: Optional[str] = None
    pin_tile: Optional[str] = None
    sou_tile: Optional[str] = None
    winning_tile: dict
    melds: Optional[List[dict]] = None
    dora_indicators: Optional[List[dict]] = None
    is_tsumo: Optional[bool] = False
    is_riichi: Optional[bool] = False

# Mahjong API
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH

app = FastAPI(
    title='my first FastAPI',
    description='ここに説明文が入る'
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/calc")
async def read_item(winning_tile: str, man_tile: str = None, pin_tile: str = None, sou_tile: str = None):
    calculator = HandCalculator()
    # アガリ形(man=マンズ, pin=ピンズ, sou=ソーズ, honors=字牌)
    tiles = TilesConverter.string_to_136_array(man=man_tile, pin=pin_tile, sou=sou_tile)

    # アガリ牌(ソーズの5)
    win_tile = TilesConverter.string_to_136_array(sou=winning_tile)[0]

    # 鳴き(チー:CHI, ポン:PON, カン:KAN(True:ミンカン,False:アンカン), カカン:CHANKAN, ヌキドラ:NUKI)
    melds = None

    # ドラ(なし)
    dora_indicators = None

    # オプション(なし)
    config = HandConfig(is_tsumo=True)

    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    return {"result_main": result.cost['main'], "result_additional": result.cost['additional'], "yaku": result.yaku}

@app.post('/calculation')
async def test(item:Item):
    calculator = HandCalculator()
    # アガリ形(man=マンズ, pin=ピンズ, sou=ソーズ, honors=字牌)
    tiles = TilesConverter.string_to_136_array(man=item.man_tile, pin=item.pin_tile, sou=item.sou_tile)

    # アガリ牌(ソーズの5)
    # TODO: ここができていない
    win_tile = TilesConverter.string_to_136_array(man=item.winning_tile['man'], pin=item.winning_tile['pin'], sou=item.winning_tile['sou'], honors=item.winning_tile['honors'])[0]

    # 鳴き(チー:CHI, ポン:PON, カン:KAN(True:ミンカン,False:アンカン), カカン:CHANKAN, ヌキドラ:NUKI)
    melds = item.melds if not None else None

    # ドラ(なし)
    dora_indicators = item.dora_indicators if not None else None

    # オプション(なし)
    config = HandConfig(is_tsumo=item.is_tsumo, is_riichi=item.is_tsumo) if not None else None

    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    return {"result_main": result.cost['main'], "result_additional": result.cost['additional'], "yaku": result.yaku}