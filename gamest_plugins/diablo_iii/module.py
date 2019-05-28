import json
import textwrap

import requests
from bs4 import BeautifulSoup

from gamest.errors import InvalidConfigurationError
from gamest.plugins import GameReporterPlugin

class DiabloIIIReporterPlugin(GameReporterPlugin):
    SETTINGS_TAB_NAME = "Diablo III"
    PATH_ENDSWITH = ['Diablo III.exe', 'Diablo III64.exe']

    def __init__(self, application):
        super().__init__(application)

        try:
            self.latest_stats = self.config.get('latest_stats', type=json.loads) or self.get_stats()
        except:
            self.latest_stats = None

        application.bind("<<GameStart{}>>".format(self.play_session.id), self.onGameStart, "+")
        application.bind("<<GameEnd{}>>".format(self.play_session.id), self.onGameEnd, "+")

        self.logger.debug("Plugin initialized.")

    @property
    def battle_net_user_name(self):
        return self.config.get('user_name', fallback=None)

    @property
    def hero_id(self):
        return self.config.get('hero_id', fallback=None)

    @classmethod
    def get_settings_template(cls):
        d = super().get_settings_template()
        d[(cls.__name__, 'user_name')] = {
            'name' : 'User name',
            'type' : 'text',
            'hint' : ("Your user name from your Battle.Net profile URL. If your "
                      "Battle.Net user name in the launcher is listed as "
                      "GamestUser#1234, then put GamestUser-1234 here.")
        }
        d[(cls.__name__, 'hero_id')] = {
            'name' : 'Hero ID',
            'type' : 'text',
            'hint' : "The ID of the hero whose paragon level you wish to track."
        }
        return d

    def get_stats(self):
        stats = {}
        if self.battle_net_user_name and self.hero_id:
            r = requests.get('https://us.diablo3.com/en/profile/{user_name}/career'.format(user_name=self.battle_net_user_name))
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                stats['lifetime_kills'] = int(soup.find('div', class_='kill-section lifetime').find('span', class_='num-kills').text)
            except:
                stats['lifetime_kills'] = 0
                logger.warning("Could not get lifetime kills.")
            try:
                stats['elite_kills'] = int(soup.find('div', class_='kill-section elite').find('span', class_='num-kills').text)
            except:
                stats['elite_kills'] = 0
                logger.warning("Could not get elite kills.")

            r = requests.get('https://us.diablo3.com/en/profile/{user_name}/hero/{hero_id}'.format(user_name=self.battle_net_user_name, hero_id=self.hero_id))
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                stats['paragon_level'] = int(soup.find('span', class_='paragon-level').text[1:-1])
            except:
                stats['paragon_level'] = 0
                logger.warning("Could not get paragon level.")

            self.config.set('latest_stats', json.dumps(stats))
        return stats

    def get_report(self):
        if not (self.battle_net_user_name and self.hero_id):
            return None
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
