#!/usr/bin/env python
import time
import pendulum
from nflapi import NFL
from nflapi.const import DIVISION_NAMES
from nflapi.__version__ import __version__ as VERSION

def schedule(nfl: NFL):
    cw = nfl.schedule.current_week()
    games=nfl.game.week_games()
    #games = nfl.game.week_games(cw.current_week['default'], cw.current_season_type['default'], cw.current_season['default'])
    tz = pendulum.tz.local_timezone()
    daylist=[]
    day1=day2=day3=day4 = []
    for game in sorted(games, key=lambda g: g.game_time):
        localtime = pendulum.instance(game.game_time).astimezone(tz)
        gamedate = "{t:%m-%d-%Y}".format(t=localtime)
        if gamedate not in daylist:
            daylist.append(gamedate)
    for game in sorted(games, key=lambda g: g.game_time):
        localtime = pendulum.instance(game.game_time).astimezone(tz)
        gamedate = "{t:%m-%d-%Y}".format(t=localtime)
        if gamedate == daylist[0]:
            day1.append(game)
        elif gamedate == daylist[1]:
            day2.append(game)
        elif gamedate == daylist[2]:
            day3.append(game)
        else:
            day4.append(game)
    def printData1(dayidx):
        gt=pendulum.instance(dayidx.game_time).astimezone(tz)
        gteams=dayidx.away_team.abbreviation+' @ '+dayidx.home_team.abbreviation
        gt="{t:%m/%d}".format(t=gt)
        gtl='  '
        gtr=' '
        if len(gteams) > 8:
            gtr='  '
        elif len(gteams) < 8:
            gtl=' '
        print(' |'+gtl+gt+gtr+'| ', end='')
    def printData2(dayidx):
        gt=pendulum.instance(dayidx.game_time).astimezone(tz)
        gteams=dayidx.away_team.abbreviation+' @ '+dayidx.home_team.abbreviation
        gtl='  '
        gtr=' '
        if len(gteams) > 8:
            gtr='  '
        elif len(gteams) < 8:
            gtl=' '
        gt="{t:%H:%M}".format(t=gt)
        print(' |'+gtl+gt+gtr+'| ', end='')
    def printData3(dayidx):
        gteams=dayidx.away_team.abbreviation+' @ '+dayidx.home_team.abbreviation
        print(' |'+gteams+'| ',end='')

    print('     ',end='')
    for i in range(0, len(day1)):
        printData1(day1[i])
    print('\n     ',end='')
    for i in range(0, len(day1)):
        printData2(day1[i])
    print('\n     ',end='')
    for i in range(0, len(day1)):
        printData3(day1[i])
    ri=input()
schedule(NFL(ua=('schedule thing')))

