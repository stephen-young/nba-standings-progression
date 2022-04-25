import pandas
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from pathlib import Path
pandas.plotting.register_matplotlib_converters()

class Group(Enum):
    EAST = auto()
    WEST = auto()
    ATLANTIC = auto()
    CENTRAL = auto()
    SOUTHEAST = auto()
    NORTHWEST = auto()
    PACIFIC = auto()
    SOUTHWEST = auto()

def standings_progression(season_year: int, group:Group):

  # Group component of basketball-reference's standings by date url
  GROUP_URL = {
      Group.EAST:      'eastern_conference',
      Group.WEST:      'western_conference',
      Group.ATLANTIC:  'atlantic_division',
      Group.CENTRAL:   'central_division',
      Group.SOUTHEAST: 'southeast_division',
      Group.NORTHWEST: 'northwest_division',
      Group.PACIFIC:   'pacific_division',
      Group.SOUTHWEST: 'southwest_division',
  }

  url = f"www.basketball-reference.com/leagues/NBA_{season_year}_standings_by_date_{GROUP_URL[group]}.html"

  standings_data = get_standings_data_from_web(url)
  standings_data = process_standings_data(standings_data)
  progression_plot = plot_standings_progression(standings_data)

  return progression_plot

def generate_standings_progression_plots(data_dir: Path, output_dir: Path) -> None:

  DATA_FILE_PATTERN = '*.xlsx'
  IMG_FORMAT = '.png'

  data_files = sorted(data_dir.glob(DATA_FILE_PATTERN))

  for file in data_files:

    try:
      ws_data = get_standings_data_from_spreadsheet(str(file))
    except:
      print("Something went wrong with " + str(file))
      continue

    win_frac_data = process_standings_data(ws_data)
    fig = plot_standings_progression(win_frac_data)
    out_file = output_dir / file.with_suffix(IMG_FORMAT).name
    fig.savefig(str(out_file), format=IMG_FORMAT[1:])


def get_standings_data_from_web(url):
  """Load standings by date data from Basketball Reference into a DataFrame from webpage
  :param url: The year of the end of the NBA regular season
  :type url: str
  :return: Standings by date data
  :rtype: pandas.DataFrame
  .. seealso:: pandas.read_html
  """

  data_frames = pandas.read_html(url, index_col=0, parse_dates=True)
  standings_data = data_frames[0]
  standings_data.columns = standings_data.columns.droplevel(0)
  standings_data = standings_data[standings_data.index.notna()]

  start_date = standings_data.index[0]
  end_date = standings_data.index[-1]
  months = pandas.date_range(start_date, end_date, freq='MS')
  months = months.strftime('%B')

  standings_data = standings_data[np.logical_not(standings_data.index.isin(months))]
  standings_data.columns = range(1, standings_data.shape[1]+1)

  return standings_data

def get_standings_data_from_spreadsheet(filename):
  """Load standings by date data from Basketball Reference into a DataFrame
  :param filename: Path to the spreadsheet file
  :type filename: str, path object or file-like object
  :return: Standings by date data
  :rtype: pandas.DataFrame
  .. seealso:: pandas.read_excel
  """

  standings_data = pandas.read_excel(filename, header=None, index_col=0, \
    parse_dates=True)
  standings_data.index.name = None

  return standings_data

def process_standings_data(standings_data):
  """Process standings data to get win fraction of teams in group by date
  :param standings_data: Table with the date and record of teams in grouping
  :type standings_data: pandas.DataFrame

  :return: Win fraction by date for each team in group
  :rtype: pandas.DataFrame
  """

  standings_data = standings_data.stack()

  standings_data = standings_data.str.extract(STANDINGS_PATTERN)

  standings_data['win'] = pandas.to_numeric(standings_data['win'])
  standings_data['loss'] = pandas.to_numeric(standings_data['loss'])
  standings_data['GP'] = standings_data['win'] + standings_data['loss']
  standings_data['PCT'] = standings_data['win'] / standings_data['GP']
  standings_data['rank'] = standings_data.index.levels[1][standings_data.index.codes[1]]
  standings_data.index = standings_data.index.droplevel(1)

  end_date = standings_data.index[-1]
  team_list = list(standings_data.loc[end_date,'team'])

  win_frac_data = [standings_data[standings_data['team'] == team]['PCT'] \
    for team in team_list]

  win_frac_df = pandas.concat(win_frac_data,axis=1,keys=team_list)

  return win_frac_df

def plot_standings_progression(data):
  """Produce a plot of the standings progression

  :param data: Win fraction by date data for each team in group
  :type data: pandas.DataFrame

  :return: Figure of standings progression plot
  :rtype: matplotlib.figure.Figure
  """

  team_list = list(data.columns)
  start_date = data.index[0]
  end_date = data.index[-1]
  dates = data.index.to_pydatetime()

  date_ticks = pandas.date_range(start_date, end_date, freq=pandas.DateOffset(months=1))

  fig, axes = plt.subplots(figsize=PLOT['Figure']['Size'])
  axes.plot(dates, data.values, linewidth=PLOT['Line']['Width'])

  # format y-axis
  axes.set_ylabel('Win fraction (wins / games played to-date)')
  axes.set_ylim(PLOT['Axes']['YMin'], PLOT['Axes']['YMax'])
  axes.set_yticks(PLOT['Axes']['YTick'])

  # format x-axis
  axes.set_xlabel('Date')
  axes.set_xlim(start_date, end_date)
  axes.set_xticks(date_ticks)

  # apply gird
  axes.grid()

  line_array = axes.get_lines()

  num_team = len(team_list)

  # Set line properties
  for i in range(num_team):
    line = line_array[i]
    team = team_list[i]
    colours = TEAM_COLOURS[team]

    line.set_label(team)
    line.set_color(colours['line'])
    line.set_marker(PLOT['Marker']['Symbol'])
    line.set_markerfacecolor(colours['marker'])
    line.set_markeredgecolor(colours['edge'])
    line.set_markeredgewidth(PLOT['Marker']['EdgeWidth'])
    line.set_markersize(PLOT['Marker']['Size'])

    # Set the line style of non-playoff teams to dotted
    if i >= 8:
      line.set_linestyle(':')

  axes.legend(ncol=PLOT['Legend']['NumCol'])
  fig.set_tight_layout(PLOT['Figure']['TightLayout'])

  return fig

STANDINGS_PATTERN = r'(?P<team>[A-Z]{3})\s\((?P<win>\d+)\-(?P<loss>\d+)\)'

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
        'YTick': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
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
