"""standings_progression_test.py is a python script used for testing module functions"""
import nba_standings_progression.nba_standings_progression as sp
import pandas as pd
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
