"""MAIN.PY is a python script used for testing module functions"""
import win_percent as wp
from pandas import date_range

filename = "2019_east_standings_by_date.xlsx"
ws_data = wp.get_standings_data_from_spreadsheet(filename)
win_frac_data = wp.process_spreadsheet_data(ws_data)
wp.plot_win_fraction_by_date(win_frac_data)

