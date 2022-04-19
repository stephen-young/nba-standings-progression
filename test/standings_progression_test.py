"""standings_progression_test.py is a python script used for testing module functions"""
import nba_standings_progression.core as sp
import matplotlib.pyplot as plt

# TODO make script a proper test for use with a testing framework (tox + pytest?)

filename = "./standings_data/2017_east_standings_by_date.xlsx"
ws_data = sp.get_standings_data_from_spreadsheet(filename)
win_frac_data = sp.process_standings_data(ws_data)

fig = sp.plot_standings_progression(win_frac_data)
plt.show()
