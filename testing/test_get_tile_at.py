from AxionsJourney import *

def test():
    p = PlayerBlock(0, 0, None, 20)
    l = Level(0, {
        "width": 5,
        "height": 5,
        "blocklist": [
            "B", "B", "B", "B", "B", 
            "B", " ", " ", " ", "B",
            "B", " ", "B", " ", "B",
            "B", " ", " ", " ", "B",
            "B", "B", "B", "B", "B", 
        ]
    })

    assert p.get_tile_at(1, 1, l) == "B"
