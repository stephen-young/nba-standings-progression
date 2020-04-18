"""MAIN.PY is a python script used for testing module functions"""
import win_percent as wp
import matplotlib.pyplot as plt

filename = "./standings_data/2017_east_standings_by_date.xlsx"
ws_data = wp.get_standings_data_from_spreadsheet(filename)
win_frac_data = wp.process_spreadsheet_data(ws_data)

fig = wp.plot_standings_progression(win_frac_data)
plt.show()
