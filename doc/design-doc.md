# Standings Progression Design Document

Stephen Young

Last updated: 26 December 2020

## Overview

I noticed that the Wikipedia pages for the NBA Playoffs of [some years had
graphs](https://en.wikipedia.org/wiki/2010_NBA_playoffs) showing the win
percentage of the playoff qualifying teams over the course of the season.
Since the graphs only showed up sporadically, I am guessing that these were
graphs made by some guy by hand with, by the look of the graphs, the 2003
version of excel. However, I thought the graphs were an nice visualisation of
how the standings settle out over the course of the season. I went looking on
[Basketball Reference](https://www.basketball-reference.com/) and found that
they have tables of the standings by date showing the position and record of
each team by date over the course of the season and could download the table
to a spreadsheet. At the time, I was also interested in learning to code in
Python and figured I could do so by making a package that would generate the
plot of the standings progression.

## Goals and Non-goals

Initially, it was intended to just be a Python package that would process the
spreadsheet downloaded from Basketball Reference. Now the goal is for the
package to scrape the data from Basketball Reference directly using the
`read_html` function from the `pandas` library. The standings progression
module will provide a a function that will take the season year and a
grouping and return a plot the standings progression of that conference for
that year. An option that the module could have is the ability to exclude
teams that miss the playoffs.

The available groupings will be:

- Conference
  - East
  - West
- Division
  - Atlantic
  - Central
  - Southeast
  - Northwest
  - Pacific
  - Southwest

Thus far, the standings progression plots have used team colours for the
markers and lines to differentiate them. It will be challenging to make the
the colour configuration for each team visually distinct enough to
differentiate between all teams when the entire league is in the plot. For
example, the Chicago Bulls, Houston Rockets, Miami Heat, Toronto Raptors have
red, white and/or black in their colours. For this reason, the largest
grouping of the standings progression plot will be a conference.
