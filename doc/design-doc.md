# Standings Progression Design Document

Stephen Young

Last updated: 16 April 2022

## Overview

I noticed that the Wikipedia pages for the NBA Playoffs of [some years had
graphs](https://en.wikipedia.org/wiki/2010_NBA_playoffs) showing the win
percentage of the playoff qualifying teams over the course of the season.
Since the graphs only showed up sporadically, I am guessing that these were
graphs made by someone manually with, by the look of the graphs, the 2003
version of excel. However, I thought the graphs were an nice visualisation of
how the standings settle out over the course of the season. I went looking on
[Basketball Reference][bballref] and found that
they have tables of the standings by date showing the position and record of
each team by date over the course of the season and could download the table
to a spreadsheet. At the time, I was also interested in learning to code in
Python and figured I could do so by making a package that would generate the
plot of the standings progression.

## Goals

- Scrape data from [Basketball Reference][bballref]
- Produce plots for Eastern and Western conferences only
- Optionally exclude teams who miss the playoffs from plot

## Non-goals

- Ignore divisions (for now)
- Ignore NBA stats API (for now)
- Ignore spreadsheet processing

## Design Intent

Initially, it was intended to just be a Python package that would process the
spreadsheet downloaded from Basketball Reference. Now the goal is for the
package to scrape the data from Basketball Reference directly using the
`read_html` function from the `pandas` library. The standings progression
module will provide a a function that will take the season end year and a
grouping and return a plot the standings progression of that conference for
that year. An option that the module could have is the ability to exclude
teams that miss the playoffs.

Thus far, the standings progression plots have used team colours for the
markers and lines to differentiate them. It will be challenging to make the
the colour configuration for each team visually distinct enough to
differentiate between all teams when the entire league is in the plot. For
example, the Chicago Bulls, Houston Rockets, Miami Heat, Toronto Raptors have
red, white and/or black in their colours. For this reason, the largest
grouping of the standings progression plot will be a conference.

I would like to include divisions but that would require more input checking
because the name and number of divisions change over the years that the
standings-by-date data is available on Basketball Reference.

It would be nice to keep the spreadsheet option available but it appears that
Basketball Reference has remove the ability to download the standings-by-date
data as a spreadsheet from the website. Consequently, it may be necessary to
deprecate the functions that read the standings-by-date data from a
spreadsheet. Maybe this would be an opportunity to add a function to write the
standings-by-date data to a spreadsheet to the module.

I understand that scrapping the data is potentially problematic for the
Basketball Reference servers and I would be interested in an API approach to
remedy this.  I am aware of packages like
[nba-api](https://pypi.org/project/nba-api/) that access the NBA's official
stats API but with a cursory glance of the documentation I was not able to see a
way to retrieve the standings progression data easily. I have not dug into the
documentation to see if I could pull the standings progression data.

[bballref]: https://www.basketball-reference.com/
