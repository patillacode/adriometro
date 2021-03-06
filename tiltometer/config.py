# DOMAIN = 'http://tilt-o-meter.patilla.es'
DOMAIN = 'http://tiltometer.lol'

PATCH_VERSION = "7.14.1"

RIOT_STATIC_SERVER_URL = "http://ddragon.leagueoflegends.com"

CHAMPION_ICON_URL = "{0}/cdn/{1}/img/champion/".format(
    RIOT_STATIC_SERVER_URL, PATCH_VERSION)
CHAMPION_SPLASH_URL = "{0}/cdn/img/champion/splash/".format(
    RIOT_STATIC_SERVER_URL)

TILT_DISPLAYS = ['thumb', 'face', 'meter']
PLAYER_POSITION = {0: 'N/A', 1: 'TOP', 2: 'MID', 3: 'JUNGLE', 4: 'BOT'}
