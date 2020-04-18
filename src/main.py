"""MAIN.PY is a python script used for testing module functions"""
import standings_progression as sp
import matplotlib.pyplot as plt

filename = "./standings_data/2017_east_standings_by_date.xlsx"
ws_data = sp.get_standings_data_from_spreadsheet(filename)
win_frac_data = sp.process_standings_data(ws_data)

fig = sp.plot_standings_progression(win_frac_data)
plt.show()
