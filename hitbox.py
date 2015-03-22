import os
import sys
import logging
import json
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen, Request, URLError


class Hitbox():

    API = 'http://api.hitbox.tv/'
    GAMES = API + 'games?liveonly=true'
    GAME_STREAMS = API + 'media/live/list?game={0}'
    CHANNELS = API + 'media/live/list'
    FOLLOWING = API + 'following/user?user_name={0}'

    CHANNEL_PLAYLIST = API + 'player/config/live/{0}'
    HLS_PLAYLIST = 'http://edge.hls.dt.hitbox.tv/hls/'

    STATIC_URL = 'http://edge.sf.hitbox.tv'

    def __init__(self, logger=logging):
        self.logger = logger
        self.scraper = JsonScraper(logger)

    def get_games(self):
        return self.scraper.get_json(self.GAMES)['categories']

    def get_game_streams(self, category_id):
        url = self.GAME_STREAMS.format(category_id)
        return self.scraper.get_json(url)

    def get_channels(self):
        return self.scraper.get_json(self.CHANNELS)

    def get_following(self, username):
        url = self.FOLLOWING.format(username)
        return self.scraper.get_json(url)

    def get_live_stream(self, channel_name, max_quality):
        json_url = self.CHANNEL_PLAYLIST.format(channel_name)
        json_data = self.scraper.get_json(json_url)
        url = self.HLS_PLAYLIST + self.__parse_bitrates(json_data['clip']['bitrates'], max_quality) + '/index.m3u8'
        return url

    def __parse_bitrates(self, bitrates, max_quality):
        bitrate_dict = {s['bitrate']: s['url'] for s in bitrates if s['label'] is not 'Auto'}
        if max_quality in bitrate_dict.keys():
            return bitrate_dict[max_quality]
        else:
            self.logger.debug('Preferred quality not available, falling back to highest')
            return bitrate_dict[max(bitrate_dict.keys())]


class JsonScraper():

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko 20100101 Firefox/6.0'}

    def __init__(self, logger=logging):
        self.logger = logger

    def get_json(self, url):
        try:
            json_string = self.get_webdata(url)
            json_dict = json.loads(json_string)
            return json_dict
        except ValueError as e:
            self.logger.error('Error parsing JSON: %s', e)
            raise HitboxException(HitboxException.JSON_ERROR)

    def get_webdata(self, url):
        try:
            request = Request(url, headers=self.HEADERS)
            response = urlopen(request)
            data = response.read() if sys.version_info < (3, 0) else response.read().decode('utf-8')
            response.close()
            return data
        except URLError as e:
            self.logger.error('Error retrieving data: %s', e)
            raise HitboxException(HitboxException.HTTP_ERROR)


class HitboxException(Exception):

    HTTP_ERROR = 0
    JSON_ERROR = 1
    STREAM_OFFLINE = 2

    def __init__(self, errno):
        self.errno = errno

    def __str__(self):
        return repr(self.errno)


if __name__ == '__main__':
    from pprint import pprint
    logging.basicConfig(filename=os.path.join(os.getcwd(), 'log'), level=1,
                        format='%(asctime)s: %(levelname)s:\t\t%(message)s', datefmt='%d.%m.%Y-%H:%M:%S')
    pprint(Hitbox().get_games())