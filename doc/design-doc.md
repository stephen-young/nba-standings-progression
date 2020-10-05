# Standings Progression Design Document

Stephen Young

Last updated: 4 October 2020

## Overview

I noticed that the Wikipedia pages for NBA Playoffs of [some years had
graphs](https://en.wikipedia.org/wiki/2010_NBA_playoffs) showing the win
percentage of the playoff qualifying teams over the course of the season.
Since the graphs only showed up sporadically, I am guessing that these were
graphs made by some guy by hand with, by the look of the graphs, the 2003
version of excel. However, I thought the graphs were an nice visualisation of
how the standings settle out over the course of the season. I went looking on
[Basketball Reference](https://www.basketball-reference.com/) and found that
they have tables of the standings by date showing the position and record of
each team by date over the course of the season and could download the table
to a spreadsheet. At the time I was also interested in learning to code in
python and figured I could do so by making a package that would generate the
plot of the standings progression.

## Goals and Non-goals

The end goal of the standings progression module will be to be able to
provide a season year and conference and for it to plot the standings
progression of that conference for that year. Some options that the module
could have is the ability to exclude teams that miss the playoffs, plot both
conferences on the same plot or two subplots beside each other.
