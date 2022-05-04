"""standings_progression_test.py is a python script used for testing module functions"""
import nba_standings_progression.nba_standings_progression as sp
import matplotlib.pyplot as plt
import pandas as pd

def test_standings_data_from_web_return_type():
    URL = "https://www.basketball-reference.com/leagues/NBA_2019_standings_by_date_eastern_conference.html"
    data = sp.get_standings_data_from_web(URL)
    assert type(data) is pd.DataFrame
