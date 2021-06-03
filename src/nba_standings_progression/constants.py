# from enum import Enum, IntEnum, auto
from numpy import linspace

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
    'LAC': {'line':'#C8102E', 'marker':'#1D428A', 'edge':'#1D428A'},
    'LAL': {'line':'#552583', 'marker':'#FDB927', 'edge':'#000000'},
    'MEM': {'line':'#5D76A9', 'marker':'#F5B112', 'edge':'#12173F'},
    'MIA': {'line':'#F9A01B', 'marker':'#98002E', 'edge':'#000000'},
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
    'UTA': {'line':'#3E2680', 'marker':'#6CAEDF', 'edge':'#00275D'},
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
        'Width': 2.0
    },
    'Marker': {
        'Symbol': '.',
        'Size': 7.5,
        'EdgeWidth': 0.25,
    },
    'Legend': {
        'NumCol': 2
    }

}
