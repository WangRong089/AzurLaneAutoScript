from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger

MAP = CampaignMap('8-3')
MAP.shape = 'H6'
MAP.map_data = '''
    MB -- ME ME ME ME -- MB
    -- ME MM ++ ++ __ ME --
    ME ++ ++ SP -- ME -- ME
    ME MA ++ -- SP ++ ME ME
    MM ME __ ME ++ ++ ME --
    MB -- ME ME ME ME -- MB
'''
MAP.weight_data = '''
    90 90 90 90 90 90 90 90
    90 90 90 90 90 90 90 05
    20 90 90 90 90 90 90 90
    25 90 90 90 90 90 90 90
    30 35 40 45 90 90 90 90
    90 90 90 90 90 90 90 90
    
'''
# MAP.camera_data = ['D3']
MAP.spawn_data = [
    {'battle': 0, 'enemy': 3},
    {'battle': 1, 'enemy': 2, 'mystery': 1},
    {'battle': 2, 'enemy': 2, 'mystery': 1},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 1, 'boss': 1},
]

A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
A6, B6, C6, D6, E6, F6, G6, H6, \
    = MAP.flatten()

road_main = RoadGrids([D5, B5, A4, A3, H3, H4])


class Config:
    INTERNAL_LINES_HOUGHLINES_THRESHOLD = 35
    EDGE_LINES_HOUGHLINES_THRESHOLD = 35
    COINCIDENT_POINT_ENCOURAGE_DISTANCE = 1.3
    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (150, 255 - 24),
        'width': (0.9, 10),
        'prominence': 10,
        'distance': 35,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (255 - 24, 255),
        'prominence': 10,
        'distance': 50,
        'width': (0, 10),
        'wlen': 1000,
    }



class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        self.fleet_2_push_forward()

        if self.clear_roadblocks([road_main]):
            return True
        if self.clear_potential_roadblocks([road_main]):
            return True

        return self.battle_default()

    def battle_4(self):
        boss = self.map.select(is_boss=True)
        if boss:
            if not self.check_accessibility(boss[0], fleet=2):
                if self.clear_roadblocks([road_main]):
                    return True

        return self.fleet_2.clear_boss()
