# NBA Standings Progression

A python library to visualize the [standings-by-date data](https://www.basketball-reference.com/leagues/NBA_2019_standings_by_date_eastern_conference.html)
from Basketball Reference in the conferences of the NBA.
Disclaimer: this library scrapes the data from Basketball Reference, please use responsibly.

```python
>>> import nba_standings_progression.nba_standings_progression as sp
>>> plot = sp.standings_progression(2019, sp.Group.EAST, sp.Inclusion.ALL)
>>> plot.show()
```
