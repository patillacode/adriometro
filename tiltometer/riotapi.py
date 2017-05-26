import requests
import time
import traceback
import urllib

import config

from flask import current_app


class RiotAPI(object):

    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = config.RIOT_REGIONS[region]
        self.game = 'lol'

    def _request(self, service, api_url, params={}):
        try:
            print 'Generating request...'
            args = {'api_key': self.api_key}
            for k, v in params.iteritems():
                if k not in args:
                    args[k] = v
            print 'args: {}'.format(args)
            # 'https://{platform}.api.riotgames.com/{game}/{service}/{version}/{resource}'
            url = config.RIOT_URL['base'].format(
                platform=self.region,
                game=self.game,
                service=service,
                version=config.RIOT_API_VERSIONS[service],
                resource=api_url)
            print 'url: {}'.format(url)
            response = requests.get(url, params=args)
            print 'Made request to: {}'.format(response.url)
            print 'Response: {}'.format(response)
            print 'Response Header: {}'.format(response.headers)
            print 'Response JSON: {}'.format(response.json())
            print 'Response STATUS: {}'.format(response.status_code)
            if response.status_code == 429:
                current_app.logger.error('{}'.format(
                    response.json()['status']['message']))
                current_app.logger.debug('Retrying in {} seconds'.format(
                    response.headers['Retry-After']))
                time.sleep(int(response.headers['Retry-After']))
                return self._request(service, api_url, params)
            return response.json()
        except:
            print traceback.format_exc()

    def get_summoner_by_name(self, summoner_name):
        print 'Getting summoner by name...'
        service_name = 'summoner-by-name'
        service = config.RIOT_SERVICES[service_name]
        api_url = urllib.quote(config.RIOT_URL[service_name].format(
            summoner_name=summoner_name))
        return self._request(service, api_url)

    def get_champions(self):
        print 'Getting champions...'
        service_name = 'champions'
        service = config.RIOT_SERVICES[service_name]
        api_url = urllib.quote(config.RIOT_URL[service_name])
        return self._request(service, api_url)

    def get_recent_matches(self, player):
        print 'Getting recent matches...'
        service_name = 'recent-matches'
        service = config.RIOT_SERVICES[service_name]
        api_url = urllib.quote(config.RIOT_URL[service_name].format(
            account_id=player['accountId']))
        return self._request(service, api_url)

    def get_match_data(self, match_id):
        print 'Getting match data...'
        service_name = 'match-data'
        service = config.RIOT_SERVICES[service_name]
        api_url = urllib.quote(config.RIOT_URL[service_name].format(
            match_id=match_id))
        return self._request(service, api_url)
