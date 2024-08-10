#! python3
# [ContextMeasure (FGM/FG3M)] [GameID] [PlayerID] [Season] [SeasonType (Regular Season/Playoffs)]
import webbrowser, sys

# Variables
context_measure = sys.argv[1]

# If 5 cmdl args, then searching for a season (not including game_id)
if len(sys.argv) == 5:
    player_id = sys.argv[2]
    season = sys.argv[3]
    season_type = sys.argv[4]
    webbrowser.open('https://www.nba.com/stats/events?CFID=&CFPARAMS=&ContextMeasure='+context_measure+'&GameID=&PlayerID='+player_id+'&Season='
                +season+'&SeasonType='+season_type+'&TeamID=&flag=3&sct=plot&section=game')
# If 6 cmdl args, then searching for a particular game (including game_id)
elif len(sys.argv) == 6:
    game_id = sys.argv[2]
    player_id = sys.argv[3]
    season = sys.argv[4]
    season_type = sys.argv[5]
    webbrowser.open('https://www.nba.com/stats/events?CFID=&CFPARAMS=&ContextMeasure='+context_measure+'&GameID='+game_id+'&PlayerID='+player_id+'&Season='
                +season+'&SeasonType='+season_type+'&TeamID=&flag=3&sct=plot&section=game')
