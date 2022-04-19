import pandas
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from nba_standings_progression.constants import TEAM_COLOURS, PLOT, STANDINGS_PATTERN, GROUP_URL
pandas.plotting.register_matplotlib_converters()

# TODO Merge constants with this(?)
# TODO Rename module to standings_progression or something
# TODO Make generate_plots.py script a function in this module

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

  url = f"www.basketball-reference.com/leagues/NBA_{season_year}_standings_by_date_{GROUP_URL[group]}"

  standings_data = get_standings_data_from_web(url)
  standings_data = process_standings_data(standings_data)
  progression_plot = plot_standings_progression(standings_data)

  return progression_plot

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
