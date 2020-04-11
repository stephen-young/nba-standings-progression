# from enum import Enum, IntEnum, auto
from numpy import linspace

"""
# Originally thought I would use enums to manage teams but just kept the strings from spreadsheet data processing
class Conference(Enum):
    East = 'East'
    West = 'West'

class Team(Enum):
    ATLANTA_HAWKS = auto()
    BOSTON_CELTICS = auto()
    BROOKLYN_NETS = auto()
    CHARLOTTE_HORNETS = auto()
    CHICAGO_BULLS = auto()
    CLEVELAND_CAVALIERS = auto()
    DALLAS_MAVERICKS = auto()
    DENVER_NUGGETS = auto()
    DETROIT_PISTONS = auto()
    GOLDEN_STATE_WARRIORS = auto()
    HOUSTON_ROCKETS = auto()
    INDIANA_PACERS = auto()
    LOS_ANGELES_CLIPPERS = auto()
    LOS_ANGELES_LAKERS = auto()
    MEMPHIS_GRIZZLIES = auto()
    MIAMI_HEAT = auto()
    MILWAUKEE_BUCKS = auto()
    MINNESOTA_TIMBERWOLVES = auto()
    NEW_ORLEANS_PELICANS = auto()
    NEW_YORK_KNICKS = auto()
    OKLAHOMA_CITY_THUNDER = auto()
    ORLANDO_MAGIC = auto()
    PHILADELPHIA_76ERS = auto()
    PHOENIX_SUNS = auto()
    PORTLAND_TRAIL_BLAZERS = auto()
    SACRAMENTO_KINGS = auto()
    SAN_ANTONIO_SPURS = auto()
    TORONTO_RAPTORS = auto()
    UTAH_JAZZ = auto()
    WASHINGTON_WIZARDS = auto()

    # HISTORICAL TEAMS
    CHARLOTTE_BOBCATS = auto()
    NEW_JERSEY_NETS = auto()
    NEW_ORLEANS_HORNETS = auto()
    NEW_ORLEANS_OKLAHOMA_CITY_HORNETS = auto()
    SEATTLE_SUPERSONICS = auto()
    VANCOUVER_GRIZZLIES = auto()

TEAM_ABBREVIATION_TO_TEAM = {
    'ATL': Team.ATLANTA_HAWKS,
    'BOS': Team.BOSTON_CELTICS,
    'BRK': Team.BROOKLYN_NETS,
    'CHI': Team.CHICAGO_BULLS,
    'CHO': Team.CHARLOTTE_HORNETS,
    'CLE': Team.CLEVELAND_CAVALIERS,
    'DAL': Team.DALLAS_MAVERICKS,
    'DEN': Team.DENVER_NUGGETS,
    'DET': Team.DETROIT_PISTONS,
    'GSW': Team.GOLDEN_STATE_WARRIORS,
    'HOU': Team.HOUSTON_ROCKETS,
    'IND': Team.INDIANA_PACERS,
    'LAC': Team.LOS_ANGELES_CLIPPERS,
    'LAL': Team.LOS_ANGELES_LAKERS,
    'MEM': Team.MEMPHIS_GRIZZLIES,
    'MIA': Team.MIAMI_HEAT,
    'MIL': Team.MILWAUKEE_BUCKS,
    'MIN': Team.MINNESOTA_TIMBERWOLVES,
    'NOP': Team.NEW_ORLEANS_PELICANS,
    'NYK': Team.NEW_YORK_KNICKS,
    'OKC': Team.OKLAHOMA_CITY_THUNDER,
    'ORL': Team.ORLANDO_MAGIC,
    'PHI': Team.PHILADELPHIA_76ERS,
    'PHO': Team.PHOENIX_SUNS,
    'POR': Team.PORTLAND_TRAIL_BLAZERS,
    'SAC': Team.SACRAMENTO_KINGS,
    'SAS': Team.SAN_ANTONIO_SPURS,
    'TOR': Team.TORONTO_RAPTORS,
    'UTA': Team.UTAH_JAZZ,
    'WAS': Team.WASHINGTON_WIZARDS,

    # HISTORICAL TEAMS
    'CHA': Team.CHARLOTTE_BOBCATS,
    'CHH': Team.CHARLOTTE_HORNETS,
    'NJN': Team.NEW_JERSEY_NETS,
    'NOH': Team.NEW_ORLEANS_HORNETS,
    'NOK': Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS,
    'SEA': Team.SEATTLE_SUPERSONICS,
    'VAN': Team.VANCOUVER_GRIZZLIES
}
"""

#Team colours selected from https://teamcolorcodes.com/nba-team-color-codes/
TEAM_COLOURS = {
    'ATL': {'line':'#E03A3E', 'marker':'#C1D32F', 'edge':'#000000'},
    'BOS': {'line':'#007A33', 'marker':'#BA9653', 'edge':'#000000'},
    'BRK': {'line':'#000000', 'marker':'#FFFFFF', 'edge':'#000000'},
    'CHI': {'line':'#000000', 'marker':'#CE1141', 'edge':'#CE1141'},
    'CHO': {'line':'#1D1160', 'marker':'#00788C', 'edge':'#000000'},
    'CLE': {'line':'#860038', 'marker':'#FDBB30', 'edge':'#000000'},
    'DAL': {'line':'#00538C', 'marker':'#002B5E', 'edge':'#000000'},
    'DEN': {'line':'#0E2240', 'marker':'#FEC524', 'edge':'#000000'},
    'DET': {'line':'#1D42BA', 'marker':'#C8102E', 'edge':'#000000'},
    'GSW': {'line':'#FFC72C', 'marker':'#1D428A', 'edge':'#1D428A'},
    'HOU': {'line':'#CE1141', 'marker':'#000000', 'edge':'#000000'},
    'IND': {'line':'#002D62', 'marker':'#FDBB30', 'edge':'#000000'},
    'LAC': {'line':'#C8102E', 'marker':'#FFFFFF', 'edge':'#000000'},
    'LAL': {'line':'#552583', 'marker':'#FDB927', 'edge':'#000000'},
    'MEM': {'line':'#5D76A9', 'marker':'#12173F', 'edge':'#000000'},
    'MIA': {'line':'#98002E', 'marker':'#F9A01B', 'edge':'#000000'},
    'MIL': {'line':'#00471B', 'marker':'#EEE1C6', 'edge':'#000000'},
    'MIN': {'line':'#236192', 'marker':'#0C2340', 'edge':'#000000'},
    'NOP': {'line':'#C8102E', 'marker':'#0C2340', 'edge':'#000000'},
    'NYK': {'line':'#006BB6', 'marker':'#F58426', 'edge':'#000000'},
    'OKC': {'line':'#007AC1', 'marker':'#EF3B24', 'edge':'#000000'},
    'ORL': {'line':'#0077C0', 'marker':'#C4CED4', 'edge':'#000000'},
    'PHI': {'line':'#006BB6', 'marker':'#ED174C', 'edge':'#000000'},
    'PHO': {'line':'#1D1160', 'marker':'#E56020', 'edge':'#000000'},
    'POR': {'line':'#000000', 'marker':'#E03A3E', 'edge':'#000000'},
    'SAC': {'line':'#5A2D81', 'marker':'#63727A', 'edge':'#000000'},
    'SAS': {'line':'#000000', 'marker':'#C4CED4', 'edge':'#000000'},
    'TOR': {'line':'#CE1141', 'marker':'#FFFFFF', 'edge':'#000000'},
    'UTA': {'line':'#00471B', 'marker':'#F9A01B', 'edge':'#002B5C'},
    'WAS': {'line':'#E31837', 'marker':'#002B5C', 'edge':'#000000'},
    'CHA': {'line':'#002B5C', 'marker':'#F58426', 'edge':'#000000'},
    'CHH': {'line':'#00778B', 'marker':'#280071', 'edge':'#000000'},
    'NJN': {'line':'#777D84', 'marker':'#002A60', 'edge':'#000000'},
    'NOH': {'line':'#00778B', 'marker':'#FFC72C', 'edge':'#000000'},
    'NOK': {'line':'#C8102E', 'marker':'#0C2340', 'edge':'#000000'},
    'SEA': {'line':'#00653A', 'marker':'#FFC200', 'edge':'#000000'},
    'VAN': {'line':'#00B2A9', 'marker':'#E43C40', 'edge':'#000000'}
}

PLOT = {
    'Figure': {
        'Size': [19.2, 10.8],
        'TightLayout': True
    },
    'Axes': {
        'YMin': 0.0,
        'YMax': 1.0,
        'YTick': linspace(0,1,11),
    },
    'Line':{
        'Marker': {
            'Symbol': 'o',
            'Size': 24.0,
            'EdgeWidth': 1.0,
        },
        'Width': 2.0
        
    },
    'Legend': {
        'NumCol': 2
    }
    
}
