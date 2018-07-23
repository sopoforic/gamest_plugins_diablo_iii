import textwrap

import requests
from bs4 import BeautifulSoup

from gamest.errors import InvalidConfigurationError
from gamest.plugins import GameReporterPlugin

class DiabloIIIReporterPlugin(GameReporterPlugin):
    PATH_ENDSWITH = ['Diablo III.exe', 'Diablo III64.exe']

    def __init__(self, application):
        super().__init__(application)

        self.battle_net_user_name = self.config.get(self.__class__.__name__, 'user_name', fallback=None)
        if not self.battle_net_user_name:
            self.logger.error("User name not set.")
            raise InvalidConfigurationError("User name not set.")
        
        self.hero_id = self.config.get(self.__class__.__name__, 'hero_id', fallback=None)
        if not self.hero_id:
            self.logger.error("Hero ID not set.")
            raise InvalidConfigurationError("Hero ID not set.")

        try:
            self.latest_stats = self.get_stats()
        except:
            self.latest_stats = None

        application.bind("<<GameEnd{}>>".format(self.play_session.id), self.onGameEnd, "+")

        self.logger.debug("Plugin initialized.")
    
    def get_stats(self):
        stats = {}
        r = requests.get('https://us.diablo3.com/en/profile/{user_name}/career'.format(user_name=self.battle_net_user_name))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        stats['lifetime_kills'] = int(soup.find('div', class_='kill-section lifetime').find('span', class_='num-kills').text)
        stats['elite_kills'] = int(soup.find('div', class_='kill-section elite').find('span', class_='num-kills').text)

        r = requests.get('https://us.diablo3.com/en/profile/{user_name}/hero/{hero_id}'.format(user_name=self.battle_net_user_name, hero_id=self.hero_id))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        stats['paragon_level'] = int(soup.find('span', class_='paragon-level').text[1:-1])

        return stats

    def get_report(self):
        stats = self.get_stats()
        if stats == self.latest_stats:
            self.logger.debug("No change found in latest_stats.")
            return None
        else:
            if self.latest_stats is None:
                self.latest_stats = stats
            diff = {
                'extra_kills' : stats['lifetime_kills'] - self.latest_stats['lifetime_kills'],
                'extra_elites' : stats['elite_kills'] - self.latest_stats['elite_kills'],
                'extra_levels' : stats['paragon_level'] - self.latest_stats['paragon_level'],
            }
            self.latest_stats = stats
            return textwrap.dedent("""\
                    Lifetime kills: {lifetime_kills:,} (**+{extra_kills:,}**)
                    Elite kills: {elite_kills:,} (**+{extra_elites:,}**)
                    Paragon level: {paragon_level:,} (**+{extra_levels:,}**)
                """.format(**stats, **diff))
