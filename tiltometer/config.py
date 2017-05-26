# DOMAIN = 'http://tilt-o-meter.patilla.es'
DOMAIN = 'http://tiltometer.lol'

PATCH_VERSION = "7.8.1"

RIOT_STATIC_SERVER_URL = "http://ddragon.leagueoflegends.com"

CHAMPION_ICON_URL = "{0}/cdn/{1}/img/champion/".format(
    RIOT_STATIC_SERVER_URL, PATCH_VERSION)
CHAMPION_SPLASH_URL = "{0}/cdn/img/champion/splash/".format(
    RIOT_STATIC_SERVER_URL)

TILT_DISPLAYS = ['thumb', 'face', 'meter']
PLAYER_POSITION = {0: 'N/A', 1: 'TOP', 2: 'MID', 3: 'JUNGLE', 4: 'BOT'}

RIOT_URL = {
    'base': 'https://{platform}.api.riotgames.com/{game}/{service}/{version}/{resource}',
    'summoner-by-name': 'summoners/by-name/{summoner_name}',
    'champions': 'champions',
    'recent-matches': 'matchlists/by-account/{account_id}/recent',
    'match-data': 'matches/{match_id}'
}

RIOT_SERVICES = {
    'summoner-by-name': 'summoner',
    'champions': 'static-data',
    'recent-matches': 'match',
    'match-data': 'match'
}

RIOT_API_VERSIONS = {
    'champion-mastery': 'v3',
    'spectator': 'v3',
    'league': 'v3',
    'static-data': 'v3',
    'lol-status': 'v3',
    'runes': 'v3',
    'masteries': 'v3',
    'match': 'v3',
    'summoner': 'v3',
    'tournament': 'v3'}

RIOT_REGIONS = {
    'br': 'br1',
    'eune': 'eun1',
    'euw': 'euw1',
    'jp': 'jp1',
    'kr': 'kr',
    'lan': 'la1',
    'las': 'la2',
    'na': 'na1',
    'oce': 'oc1',
    'tr': 'tr1',
    'ru': 'ru',
    'pbe': 'pbe1'}
