import os

import pytest
import requests_cache

from gamest_plugins.diablo_iii.module import DiabloIIIReporterPlugin

requests_cache.install_cache('test_cache', expire_after=3600)

def test_get_stats_lifetime_kills():
    stats = DiabloIIIReporterPlugin._get_stats('Achilles-1743', '75522659')
    assert stats['lifetime_kills'] != 0

def test_get_stats_elite_kills():
    stats = DiabloIIIReporterPlugin._get_stats('Achilles-1743', '75522659')
    assert stats['elite_kills'] != 0

def test_get_stats_paragon_level():
    stats = DiabloIIIReporterPlugin._get_stats('Achilles-1743', '75522659')
    assert stats['paragon_level'] != 0
