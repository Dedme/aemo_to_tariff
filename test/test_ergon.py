import unittest
from datetime import datetime, time
from zoneinfo import ZoneInfo

from aemo_to_tariff.ergon import (
    time_zone,
    get_daily_fee,
    calculate_demand_fee,
    get_periods,
    convert_feed_in_tariff,
    convert,
)

class TestErgonFunctions(unittest.TestCase):
    def test_time_zone(self):
        self.assertEqual(time_zone(), 'Australia/Brisbane')

    def test_get_daily_fee(self):
        self.assertEqual(get_daily_fee('ERDEMT1'), 1.208)
        self.assertEqual(get_daily_fee('EBDEMT1'), 1.260)

    def test_calculate_demand_fee(self):
        self.assertAlmostEqual(calculate_demand_fee('ERDEMT1', 10, 30), 74.271)
        self.assertAlmostEqual(calculate_demand_fee('EBDEMT1', 5, 15), 18.015)
      
    def test_get_periods(self):
        periods = get_periods('ERDEMT1')
        self.assertEqual(len(periods), 1)
        self.assertEqual(periods[0], ('Anytime', time(0, 0), time(23, 59), 4.262))
        with self.assertRaises(ValueError):
            get_periods('UNKNOWN')

    def test_convert_feed_in_tariff(self):
        interval_datetime = datetime(2023, 1, 1, 12, 0, tzinfo=ZoneInfo('Australia/Brisbane'))
        self.assertEqual(convert_feed_in_tariff(interval_datetime, 'ERDEMT1', 100), 10.0)

    def test_convert(self):
        interval_datetime = datetime(2023, 1, 1, 12, 0, tzinfo=ZoneInfo('Australia/Brisbane'))
        self.assertAlmostEqual(convert(interval_datetime, 'ERDEMT1', 100), 14.262)
        self.assertAlmostEqual(convert(interval_datetime, 'ERDEMT2', 100), 14.091)
