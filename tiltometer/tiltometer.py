import datetime
import random
# import sys
import traceback

import config

from flask import current_app

from keys import API_KEY
from tilt_exceptions import SummonerNotFound

from riotapi import RiotAPI


def get_champions_data(api):
    # champions_list = watcher.static_get_champion_list()['data']
    champions = api.get_champions()['data']
    champions_dict = {}
    for data in champions.values():
        champions_dict[data['id']] = {'name': data['name'], 'key': data['key']}

    return champions_dict


def get_champion_name_by_id(champion_id, champions_dict):
    return champions_dict[champion_id]['name']


def get_champion_key_by_id(champion_id, champions_dict):
    return champions_dict[champion_id]['key']


def get_stats(games, champions_dict):
    stats = []

    for game in games:
        kills = game['stats'].get('championsKilled', 0)
        deaths = game['stats'].get('numDeaths', 0)
        assists = game['stats'].get('assists', 0)

        champion_name = get_champion_name_by_id(game['championId'],
                                                champions_dict)
        champion_key = get_champion_key_by_id(game['championId'],
                                              champions_dict)
        champion_img = '{0}{1}.png'.format(config.CHAMPION_ICON_URL,
                                           champion_key)
        position = game['stats'].get('playerPosition', 0)
        pentakill = True if game['stats'].get('largestMultiKill', 0) == 5 \
            else False

        time = game['stats']['timePlayed']
        game_type = game['subType']
        win = False

        if game['stats']['win']:
            win = True

        date = datetime.datetime.fromtimestamp(game['createDate'] / 1000)
        date = date.strftime('%d/%b %H:%M')

        g = {'kills': kills,
             'deaths': deaths,
             'assists': assists,
             'champion_name': champion_name,
             'champion_img': champion_img,
             'position': config.PLAYER_POSITION[position],
             'pentakill': pentakill,
             'time': '{0}:{1}'.format(time / 60, str(time % 60).zfill(2)),
             'game_type': game_type,
             'win': win,
             'date': date}

        stats.append(g)

    return stats


def get_wins_number(games, summoner_name):
    print 'get_wins_number...'
    wins_number = 0
    try:
        for game in games:
            for player in game['participantIdentities']:
                if player['player']['summonerName'] == summoner_name:
                    player_id = int(player['participantId'])
                    print 'player_id = {}'.format(player_id)

            if player_id < 6:
                team = 0
            else:
                team = 1

            if game['teams'][team]['win'] == "Win":
                wins_number += 1
        print 'wins = {}'.format(wins_number)
        return wins_number
    except:
        current_app.logger.debug(traceback.format_exc())
        print traceback.format_exc()


def get_random_background_url(champions_dict):
    random_champion_name = random.sample(champions_dict.values(), 1)[0]['key']
    return "{0}{1}_0.jpg".format(config.CHAMPION_SPLASH_URL,
                                 random_champion_name)


def get_random_display():
    return random.choice(config.TILT_DISPLAYS)


def get_kda(kills, deaths, assists):
    return (kills + deaths) / max(1, deaths)


def get_tilt_level(games):
    # this is a subjective algorithm to measure someone's tilt
    # completely arbitrary - over a 100 point scale
    tilt_points = 0
    multiplier = 10
    cold_streak = 0

    for game in games:
        # When practising vs BOTS or custom games you never get tilted,
        # so they don't count. We even take 3 points off the tilt level,
        # since they are just for fun
        if ('BOT' or 'NONE') in game['role']:
            tilt_points -= 3
            continue

        this_game_tilt_points = 0

        if not game['stats']['win']:
            # 0.5 tilt points for every game lost
            # bigger multiplier the more recent the game was
            this_game_tilt_points += multiplier
            tilt_points += multiplier
            # add cold streak
            cold_streak += 1

            # if you lost a game under 25 minutes probably means you forfited
            # or you were crushed
            # multiplier for the more recent the game was
            if game['stats']['timePlayed'] < 1500:
                tilt_points += multiplier
                this_game_tilt_points += multiplier
        else:
            cold_streak = 0
            # you won the game, that should count for something right?
            tilt_points -= 5
            this_game_tilt_points -= 5
            # if you won a game under 25 minutes probably means the
            # opponents forfited or you crushed them
            # multiplier for the more recent the game was
            if game['stats']['timePlayed'] < 1500:
                tilt_points -= multiplier
                this_game_tilt_points -= multiplier

        # if you lost 2 or more games in a row you gain tilt points per game
        # bigger multiplier the more recent the cold strike was
        if cold_streak > 1:
            tilt_points += cold_streak * (multiplier)

            this_game_tilt_points += cold_streak * (multiplier)

        kda = get_kda(game['stats'].get('championsKilled', 0),
                      game['stats'].get('numDeaths', 0),
                      game['stats'].get('assists', 0))

        # if your KDA is low... tilt points for you!
        if kda < 1:
            # tilt_points += 1.25 * multiplier
            tilt_points += 8
            # this_game_tilt_points += 1.25 * multiplier
            this_game_tilt_points += 8
        elif kda < 2:
            # tilt_points += 0.75 * multiplier
            tilt_points += 3
            # this_game_tilt_points += 0.75 * multiplier
            this_game_tilt_points += 3
        elif kda < 3:
            tilt_points += 1
            this_game_tilt_points += 1
        else:
            # if your kda is over 3 you did very well and you are happy
            # let's get some tilt point off of you ^^
            # tilt_points -= multiplier
            tilt_points -= 3
            # this_game_tilt_points -= multiplier
            this_game_tilt_points -= 3

        # When playing a normal game tilt exists but is not the same as rankeds
        # since you play just to practice, sometimes troll etc...
        if 'NORMAL' in game['subType']:
            tilt_points -= (this_game_tilt_points / 3)

        multiplier -= 1

    if tilt_points > 100:
        return 100
    elif tilt_points < 1:
        return 0

    return tilt_points


def get_tilt(area, summoner_name):
    try:
        api = RiotAPI(API_KEY, area)
        champions_dict = get_champions_data(api)
        try:
            player = api.get_summoner_by_name(summoner_name)
        except:
            current_app.logger.debug('Summoner {0} not found.'.format(
                summoner_name))
            raise SummonerNotFound(
                'Summoner {0} not found in {1} server.'.format(
                    summoner_name, area.upper()))
        # last 20 matches - overview, no specifics
        recent_matches = api.get_recent_matches(player)['matches']

        recent_games = []

        max_matches = 2
        aux = 0
        for match in recent_matches:
            if aux < max_matches:
                recent_games.append(api.get_match_data(match['gameId']))
                aux += 1
            else:
                break

        # print 'RECENT_GAMES: {}'.format(recent_games)
        for rg in recent_games:
            print '#' * 60
            print rg
        print 'RECENT_GAMES: {}'.format(len(recent_games))
        try:
            response = {"status": 200,
                        "wins": get_wins_number(recent_games, summoner_name),
                        "metadata": {
                            "background": get_random_background_url(
                                champions_dict),
                            "display": get_random_display()},
                        "stats": get_stats(recent_games, champions_dict),
                        "summoner_name": summoner_name,
                        "tilt_level": get_tilt_level(recent_games)}
        except:
            traceback.format_exc()

        return response
    except:
        current_app.logger.error(traceback.format_exc())
        raise
