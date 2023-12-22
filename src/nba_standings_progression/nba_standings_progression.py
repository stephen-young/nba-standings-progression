import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as matdates
from enum import Enum, auto

pandas.plotting.register_matplotlib_converters()


class Group(Enum):
    EAST = auto()
    WEST = auto()


def standings_progression(
    year: int, group: Group
) -> plt.Figure:
    """Create standings progression plot

    Standings progression plot is created for the desired group in the chosen
    season using standings by date data on Basketball Reference

    Args:
      year (int): end year of the NBA season
      group (Group): team grouping to plot standings progression
      include (Inclusion): team inclusion in plot

    Returns:
      Figure: Figure of standings progression plot
    """

    url = get_standings_data_url(year, group)
    standings_data = get_standings_data_from_web(url)
    standings_data = process_standings_data(standings_data)
    progression_plot = plot_standings_progression(standings_data)

    return progression_plot


def get_standings_data_url(year: int, group: Group) -> str:
    """Creates url with the standings by date data

    Args:
        year (int): end year of NBA season
        group (Group): team grouping

    Returns:
        str: url of standings by date data
    """

    BASE_URL = "https://www.basketball-reference.com"
    GROUP_URL = {Group.EAST: "eastern_conference", Group.WEST: "western_conference"}
    url = f"{BASE_URL}/leagues/NBA_{year}_standings_by_date_{GROUP_URL[group]}.html"

    return url


def get_standings_data_from_web(url):
    """Create standings by date DataFrame

    Args:
      url (str): url to a standings-by-date basketball reference page

    Returns:
      DataFrame: Standings by date data

    Raises:
      HTTPError: An HTTP Error 404 is raised if url is not found
    """

    # Scrape standings-by-date data
    data_frames = pandas.read_html(url, index_col=0, parse_dates=True)

    # Page should only have one table so first entry is extracted
    standings_data = data_frames[0]

    # DataFrame comes in with the first month of the season included in a
    # multilevel column and the intervening months as rows
    standings_data.columns = standings_data.columns.droplevel(0)

    # Remove N/A entries
    standings_data = standings_data[standings_data.index.notna()]

    # Determine intervening months in the data set
    start_date = standings_data.index[0]
    end_date = standings_data.index[-1]
    months = pandas.date_range(start_date, end_date, freq="MS")
    months = months.strftime("%B")

    # Remove rows that are just month names
    standings_data = standings_data[
        numpy.logical_not(standings_data.index.isin(months))
    ]
    # Set columns to rank number
    standings_data.columns = range(1, standings_data.shape[1] + 1)
    standings_data.index = pandas.to_datetime(standings_data.index)

    return standings_data


def process_standings_data(standings_data):
    """Process standings data to get win fraction of teams in group by date

    Args:
      standings_data (DataFrame): standings-by-date data from basketball reference

    Returns:
      DataFrame: Win fraction by date for each team in group
    """

    STANDINGS_PATTERN = r"(?P<team>[A-Z]{3})\s\((?P<win>\d+)\-(?P<loss>\d+)\)"

    standings_data = standings_data.stack()
    standings_data.index = standings_data.index.rename(("date", "rank"))

    standings_data = standings_data.str.extract(STANDINGS_PATTERN)

    standings_data["win"] = pandas.to_numeric(standings_data["win"])
    standings_data["loss"] = pandas.to_numeric(standings_data["loss"])
    standings_data["GP"] = standings_data["win"] + standings_data["loss"]
    standings_data["PCT"] = standings_data["win"] / standings_data["GP"]
    standings_data = standings_data.reset_index(level="rank")
    standings_data = standings_data.drop_duplicates(subset=["team", "GP"])

    return standings_data


def plot_standings_progression(standings_data):
    """Produce a plot of the standings progression

    Args:
      data (DataFrame): Win fraction by date data for each team in group
      max_rank (int): rank in final standings cut-off for inclusion in plot
      dash_rank (int): rank in final standings cut-off to plot with solid line

    Returns:
      Figure: Figure of standings progression plot
    """

    standings_data = standings_data.reset_index()

    final_standings = standings_data[standings_data["GP"] == standings_data["GP"].max()]
    final_standings = final_standings.sort_values(by="rank")
    final_standings = final_standings.set_index("team")
    team_list = final_standings.index

    start_date = standings_data["date"].min()
    end_date = standings_data["date"].max()
    date_ticks = pandas.date_range(
        start_date, end_date, freq=pandas.DateOffset(months=1)
    )

    fig, axes = plt.subplots(figsize=PLOT["Figure"]["Size"])

    # format y-axis
    axes.set_ylabel("Win fraction (wins / games played to-date)")
    axes.set_ylim(PLOT["Axes"]["YMin"], PLOT["Axes"]["YMax"])
    axes.set_yticks(PLOT["Axes"]["YTick"])

    # format x-axis
    axes.set_xlabel("Date")
    axes.set_xlim(start_date, end_date)
    axes.set_xticks(date_ticks)
    axes.xaxis.set_major_formatter(matdates.DateFormatter("%Y-%m-%d"))

    # apply gird
    axes.grid()

    for team in team_list:
        colours = TEAM_COLOURS[team]
        team_data = standings_data[standings_data["team"] == team]
        style = "-"

        axes.plot(
            "date",
            "PCT",
            data=team_data,
            label=team,
            color=colours["line"],
            linewidth=PLOT["Line"]["Width"],
            linestyle=style,
            marker=PLOT["Marker"]["Symbol"],
            markeredgecolor=colours["edge"],
            markerfacecolor=colours["marker"],
            markeredgewidth=PLOT["Marker"]["EdgeWidth"],
            markersize=PLOT["Marker"]["Size"],
        )

    axes.legend(ncol=PLOT["Legend"]["NumCol"])
    fig.set_tight_layout(PLOT["Figure"]["TightLayout"])

    return fig


# Team colours selected from https://teamcolorcodes.com/nba-team-color-codes/
TEAM_COLOURS = {
    "ATL": {"line": "#E03A3E", "marker": "#C1D32F", "edge": "#000000"},
    "BOS": {"line": "#007A33", "marker": "#BA9653", "edge": "#000000"},
    "BRK": {"line": "#000000", "marker": "#FFFFFF", "edge": "#000000"},
    "CHI": {"line": "#000000", "marker": "#CE1141", "edge": "#CE1141"},
    "CHO": {"line": "#1D1160", "marker": "#00788C", "edge": "#000000"},
    "CLE": {"line": "#860038", "marker": "#FDBB30", "edge": "#000000"},
    "DAL": {"line": "#00538C", "marker": "#002B5E", "edge": "#000000"},
    "DEN": {"line": "#0E2240", "marker": "#FEC524", "edge": "#000000"},
    "DET": {"line": "#1D42BA", "marker": "#C8102E", "edge": "#000000"},
    "GSW": {"line": "#FFC72C", "marker": "#1D428A", "edge": "#1D428A"},
    "HOU": {"line": "#CE1141", "marker": "#000000", "edge": "#000000"},
    "IND": {"line": "#002D62", "marker": "#FDBB30", "edge": "#000000"},
    "LAC": {"line": "#C8102E", "marker": "#1D428A", "edge": "#1D428A"},
    "LAL": {"line": "#552583", "marker": "#FDB927", "edge": "#000000"},
    "MEM": {"line": "#5D76A9", "marker": "#F5B112", "edge": "#12173F"},
    "MIA": {"line": "#F9A01B", "marker": "#98002E", "edge": "#000000"},
    "MIL": {"line": "#00471B", "marker": "#EEE1C6", "edge": "#000000"},
    "MIN": {"line": "#236192", "marker": "#0C2340", "edge": "#000000"},
    "NOP": {"line": "#C8102E", "marker": "#0C2340", "edge": "#000000"},
    "NYK": {"line": "#006BB6", "marker": "#F58426", "edge": "#000000"},
    "OKC": {"line": "#007AC1", "marker": "#EF3B24", "edge": "#000000"},
    "ORL": {"line": "#0077C0", "marker": "#C4CED4", "edge": "#000000"},
    "PHI": {"line": "#006BB6", "marker": "#ED174C", "edge": "#000000"},
    "PHO": {"line": "#1D1160", "marker": "#E56020", "edge": "#000000"},
    "POR": {"line": "#000000", "marker": "#E03A3E", "edge": "#000000"},
    "SAC": {"line": "#5A2D81", "marker": "#63727A", "edge": "#000000"},
    "SAS": {"line": "#000000", "marker": "#C4CED4", "edge": "#000000"},
    "TOR": {"line": "#CE1141", "marker": "#FFFFFF", "edge": "#000000"},
    "UTA": {"line": "#3E2680", "marker": "#6CAEDF", "edge": "#00275D"},
    "WAS": {"line": "#E31837", "marker": "#002B5C", "edge": "#000000"},
    "CHA": {"line": "#002B5C", "marker": "#F58426", "edge": "#000000"},
    "CHH": {"line": "#00778B", "marker": "#280071", "edge": "#000000"},
    "NJN": {"line": "#777D84", "marker": "#002A60", "edge": "#000000"},
    "NOH": {"line": "#00778B", "marker": "#FFC72C", "edge": "#000000"},
    "NOK": {"line": "#C8102E", "marker": "#0C2340", "edge": "#000000"},
    "SEA": {"line": "#00653A", "marker": "#FFC200", "edge": "#000000"},
    "VAN": {"line": "#00B2A9", "marker": "#E43C40", "edge": "#000000"},
}

PLOT = {
    "Figure": {"Size": [14.4, 8.1], "TightLayout": True},
    "Axes": {
        "YMin": 0.0,
        "YMax": 1.0,
        "YTick": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    },
    "Line": {"Width": 2.0},
    "Marker": {
        "Symbol": ".",
        "Size": 7.5,
        "EdgeWidth": 0.25,
    },
    "Legend": {"NumCol": 2},
}
