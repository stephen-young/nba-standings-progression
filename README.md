# NBA Standings Progression

Visualize the progression of season standings in the conferences of the NBA.

```python
>>> import nba_standings_progression.nba_standings_progression  as sp
>>> plot = sp.standings_progression(2019, sp.Group.EAST, sp.Inclusion.ALL)
>>> plot.show()
```
