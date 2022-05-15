"""standings_progression_test.py is a python script used for testing module functions"""
import nba_standings_progression.nba_standings_progression as sp
import pandas as pd
import matplotlib.pyplot as plt
import pytest
import numpy

@pytest.fixture(scope="session")
def standings_data():
    URL = "https://www.basketball-reference.com/leagues/NBA_2019_standings_by_date_eastern_conference.html"
    data = sp.get_standings_data_from_web(URL)
    return data

@pytest.fixture(scope="session")
def processed_data(standings_data):
    return sp.process_standings_data(standings_data)

def test_standings_data_from_web_return_type(standings_data):
    assert type(standings_data) is pd.DataFrame

def test_standings_data_from_web_shape(standings_data):
    assert standings_data.shape == (168, 15)

def test_processed_standings_data_return_type(processed_data):
    assert type(processed_data) is pd.DataFrame

def test_processed_standings_data_shape(processed_data):
    assert processed_data.shape == (15*82, 6)

def test_processed_standings_data_result(processed_data):
    final_standings = processed_data[processed_data['GP'] == processed_data['GP'].max()]
    final_standings = final_standings.sort_values(by='rank')
    assert all(final_standings['rank'] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    assert all(final_standings['team'] == ['MIL', 'TOR', 'PHI', 'BOS', 'IND', 'BRK', 'ORL', 'DET', 'CHO', 'MIA', 'WAS', 'ATL', 'CHI', 'CLE', 'NYK'])
    assert all(final_standings['win'] == [60, 58, 51, 49, 48, 42, 42, 41, 39, 39, 32, 29, 22, 19, 17])
    assert all(final_standings['loss'] == [22, 24, 31, 33, 34, 40, 40, 41, 43, 43, 50, 53, 60, 63, 65])
    assert numpy.allclose(final_standings['PCT'] , [0.732, 0.707, 0.622, 0.598, 0.585, 0.512, 0.512, 0.500, 0.476, 0.476, 0.390, 0.354, 0.268, 0.232, 0.207], rtol=1e-2)

def test_plot_standings_progression_return_type(processed_data):
    standings_plot = sp.plot_standings_progression(processed_data)
    assert type(standings_plot) is plt.Figure

def standings_plot_check(plot, line_count_exp, line_label_exp, line_style_exp):
    axes = plot.get_axes()
    axes = axes[0]
    lines = axes.get_lines()
    line_labels = [line.get_label() for line in lines]
    line_styles = [line.get_linestyle() for line in lines]
    assert len(lines) == line_count_exp
    assert line_labels == line_label_exp
    assert line_styles == line_style_exp

def test_plot_standings_progression_defaults(processed_data):
    standings_plot = sp.plot_standings_progression(processed_data)
    exp_line_count = 15
    exp_line_labels = ['MIL', 'TOR', 'PHI', 'BOS', 'IND', 'BRK', 'ORL', 'DET', 'CHO', 'MIA', 'WAS', 'ATL', 'CHI', 'CLE', 'NYK']
    exp_line_styles = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    standings_plot_check(standings_plot, exp_line_count, exp_line_labels, exp_line_styles)

def test_plot_standings_progression_dashed(processed_data):
    standings_plot = sp.plot_standings_progression(processed_data, dash_rank = 8)
    exp_line_count = 15
    exp_line_labels = ['MIL', 'TOR', 'PHI', 'BOS', 'IND', 'BRK', 'ORL', 'DET', 'CHO', 'MIA', 'WAS', 'ATL', 'CHI', 'CLE', 'NYK']
    exp_line_styles = ['-', '-', '-', '-', '-', '-', '-', '-', ':', ':', ':', ':', ':', ':', ':']
    standings_plot_check(standings_plot, exp_line_count, exp_line_labels, exp_line_styles)

def test_plot_standings_progression_exclusion(processed_data):
    standings_plot = sp.plot_standings_progression(processed_data, max_rank = 8)
    exp_line_count = 8
    exp_line_labels = ['MIL', 'TOR', 'PHI', 'BOS', 'IND', 'BRK', 'ORL', 'DET']
    exp_line_styles = ['-', '-', '-', '-', '-', '-', '-', '-']
    standings_plot_check(standings_plot, exp_line_count, exp_line_labels, exp_line_styles)

