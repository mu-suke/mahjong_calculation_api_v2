# FastAPI
from fastapi import FastAPI
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

    # 鳴き(なし)
    melds = None

    # ドラ(なし)
    dora_indicators = None

    # オプション(なし)
    config = HandConfig(is_tsumo=True)

    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    return {"result_main": result.cost['main'], "result_additional": result.cost['additional'], "yaku": result.yaku}

