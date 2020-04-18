import pandas
import matplotlib.pyplot as plt
from constants import TEAM_COLOURS, PLOT
pandas.plotting.register_matplotlib_converters()

def get_standings_data_from_spreadsheet(filename):

  col_names = ['1st','2nd', '3rd', '4th', '5th','6th', '7th', '8th','9th', \
    '10th', '11th', '12th', '13th', '14th', '15th']

  standings_data = pandas.read_excel(filename, header=None, index_col=0, \
    parse_dates=True, names=col_names)

  standings_data = standings_data.stack()

  standings_pattern = r'(?P<team>[A-Z]{3})\s\((?P<win>\d+)\-(?P<loss>\d+)\)'

  standings_data = standings_data.str.extract(standings_pattern)

  standings_data['win'] = pandas.to_numeric(standings_data['win'])
  standings_data['loss'] = pandas.to_numeric(standings_data['loss'])
  standings_data['GP'] = standings_data['win'] + standings_data['loss']
  standings_data['PCT'] = standings_data['win'] / standings_data['GP']
  standings_data['rank'] = standings_data.index.levels[1][standings_data.index.codes[1]]
  standings_data.index = standings_data.index.droplevel(1)

  return standings_data 

def process_spreadsheet_data(standings_data):

  end_date = standings_data.index[-1]
  team_list = list(standings_data.loc[end_date,'team'])

  win_frac_data = [standings_data[standings_data['team'] == team]['PCT'] \
    for team in team_list]

  win_frac_df = pandas.concat(win_frac_data,axis=1,keys=team_list)
  
  return win_frac_df

def plot_standings_progression(data):

  # // put magic numbers into a dict in constants.py

  team_list = list(data.columns)
  start_date = data.index[0]
  end_date = data.index[-1]
  dates = data.index.to_pydatetime()

  # // make x-ticks 1 month offsets from start date rather than the start of each month
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
    line.set_marker('.')
    line.set_markerfacecolor(colours['marker'])
    line.set_markeredgecolor(colours['edge'])
    line.set_markeredgewidth(0.25)
    line.set_markersize(7.5)

    # Set the line style of non-playoff teams to dotted
    if i >= 8:
      line.set_linestyle(':')

  axes.legend(ncol=PLOT['Legend']['NumCol'])
  fig.set_tight_layout(PLOT['Figure']['TightLayout'])

  return fig
