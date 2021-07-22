#!/usr/bin/env python
from nflapi import *
from nflapi.helpers import *
import pendulum
import os
import sys
import subprocess
import urwid
from pathlib import Path
from functools import partial
homepath = str(Path.home())
homeFile = homepath+"/.rosterizer/home.txt"
awayFile = homepath+"/.rosterizer/away.txt"
if not os.path.isdir(homepath+'/.rosterizer/'):
    os.system("mkdir ~/.rosterizer")
os.system("touch ~/.rosterizer/home.txt; touch ~/.rosterizer/away.txt")

tz = pendulum.tz.local_timezone()
nowtime=pendulum.now()

#this is just for testing:
#nowtime = nowtime.add(days=-11)
def getTerminalSize():
    import shlex
    import struct
    import platform
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

termSize = getTerminalSize()

nfl=NFL(ua='Rosterizer')

def getRoster(teamabbr):
    return RosterHelper(nfl).lookup(teamabbr)

def keyHandler(k):
    if k == 'j':
        os.system("2>/dev/null 1>/dev/null ydotool key Down")
    elif k == 'k':
        os.system("2>/dev/null 1>/dev/null ydotool key Up")
    elif k == 'q':
        raise urwid.ExitMainLoop()

def getTodayGames():
    # this is shitty, it should accept team names or a team name
    todayGames=[]
    cw = nfl.schedule.current_week()
    games = nfl.game.week_games(cw.week_value, cw.season_type, cw.season_value)
    if len(sys.argv) == 1:
        for game in sorted(games, key=lambda g: g.game_time):
            localtime = pendulum.instance(game.game_time).astimezone(tz)
            if nowtime.diff(localtime).in_days() < 1:
                todayGames.append(game)
    else:
        for game in sorted(games, key=lambda g: g.game_time):
            localtime = pendulum.instance(game.game_time).astimezone(tz)
            todayGames.append(game)
    return todayGames

def menu(title, todaygames):
    body = [urwid.Text(title)]
    for g in todaygames:
        gametime=pendulum.instance(g.game_time).astimezone(tz).format('h:mm A')
        buttontitle=g.home_team.abbreviation+" vs. "+g.away_team.abbreviation
        #I should take terminal width into account here for the spacer
        spacer =" "*(26-len(buttontitle+" "+gametime))
        #spacer =" "*(int(termSize[0]*0.5)-len(buttontitle+" "+gametime))
        button = urwid.Button(buttontitle+spacer+gametime)
        urwid.connect_signal(button, 'click', makeFileAndVimIt, g)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def makeFileAndVimIt(button, selectedGame):
    homeAbbr=selectedGame.home_team.abbreviation
    awayAbbr=selectedGame.away_team.abbreviation
    def makeRosterDict(abb):
        rosterDict={}
        for item in getRoster(abb):
            if str(item.jersey_number).isalpha():
                rosterDict[0]=item.first_name + " " + item.last_name
            else:
                rosterDict[item.jersey_number]=item.first_name + " " + item.last_name
        return rosterDict
    def writeFile(roster, home):
        if home:
            target = homeFile
        else:
            target = awayFile
        open(target, 'w').close()
        with open(target, 'r+') as tfile:
            if home:
                tfile.write(homeAbbr+"\n\n")
            else:
                tfile.write(awayAbbr+"\n\n")
            for i in sorted(roster):
                tfile.write(str(i) + " " + roster[i] + "\n")
    homeRoster=makeRosterDict(homeAbbr)
    awayRoster=makeRosterDict(awayAbbr)
    writeFile(homeRoster, True)
    writeFile(awayRoster, False)
    os.system("vim -O " + homeFile + " " + awayFile)
    raise urwid.ExitMainLoop()
try:
    main = urwid.Padding(menu(u'Today\'s Games', getTodayGames()), left=1, right=1)
except:
    print("no internet!")
    main = urwid.Padding(menu(u'No Internet', {}), left=1, right=1)

top = urwid.Overlay(main, urwid.SolidFill(u'\N{LIGHT SHADE}'),
    align='center', width=('relative', termSize[0]),
    valign='middle', height=('relative', termSize[1]),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')], unhandled_input=keyHandler).run()
