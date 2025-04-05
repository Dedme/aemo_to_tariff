from datetime import time, datetime
from zoneinfo import ZoneInfo

def time_zone():
    return 'Australia/Brisbane'

daily_fees = {
    'ERDEMT1': 1.208,
    'ERDEMT2': 1.208,
    'ERDEMT3': 1.208,
    'EBDEMT1': 1.260,
    'EBDEMT2': 1.260,
    'EBDEMT3': 1.260,
}

demand_charges = {
    'ERDEMT1': 0.24757,
    'ERDEMT2': 0.2576,
    'ERDEMT3': 0.2525,
    'EBDEMT1': 0.2402,
    'EBDEMT2': 0.24857,
    'EBDEMT3': 0.2536,
}

tariffs = {
    'ERDEMT1': {
        'name': 'Residential Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 4.262)],
        'rate': 4.262
    },
    'ERDEMT2': {
        'name': 'Residential Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 4.091)],
        'rate': 4.091
    },
    'ERDEMT3': {
        'name': 'Residential Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 4.21)],
        'rate': 4.21
    },
    'EBDEMT1': {
        'name': 'Small Business Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 0.0)],
        'rate': 0.0
    },
    'EBDEMT2': {
        'name': 'Small Business Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 0.0)],
        'rate': 0.0
    },
    'EBDEMT3': {
        'name': 'Small Business Demand',
        'periods': [('Anytime', time(0, 0), time(23, 59), 0.0)],
        'rate': 0.0
    },
    'ELFLEXT1': {
        'name': 'Dynamic Flex TOU',
        'periods': [
            ('Peak', time(17, 0), time(21, 0), 2.04),
            ('Shoulder', time(7, 0), time(17, 0), 2.04),
            ('Off-Peak', time(21, 0), time(7, 0), 2.04)
        ],
        'rate': {'Peak': 2.04, 'Shoulder': 2.04, 'Off-Peak': 2.04}
    },
    'ECFLEXT1': {
        'name': 'Dynamic Flex TOU',
        'periods': [
            ('Peak', time(17, 0), time(21, 0), 1.227),
            ('Shoulder', time(7, 0), time(17, 0), 1.227),
            ('Off-Peak', time(21, 0), time(7, 0), 1.227)
        ],
        'rate': {'Peak': 1.227, 'Shoulder': 1.227, 'Off-Peak': 1.227}
    },
    'ECPRCET1': {
        'name': 'Dynamic Flex TOU',
        'periods': [
            ('Peak', time(17, 0), time(21, 0), 1.227),
            ('Shoulder', time(7, 0), time(17, 0), 1.227),
            ('Off-Peak', time(21, 0), time(7, 0), 1.227)
        ],
        'rate': {'Peak': 1.227, 'Shoulder': 1.227, 'Off-Peak': 1.227}
    }
}

def get_daily_fee(tariff_code: str, annual_usage: float = None):
    return daily_fees.get(tariff_code, 0.0)

def calculate_demand_fee(tariff_code: str, demand_kw: float, days: int = 30):
    if tariff_code not in demand_charges:
        return 0.0
    daily_rate = demand_charges[tariff_code]
    return daily_rate * demand_kw * days

def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")
    return tariff['periods']

def convert_feed_in_tariff(interval_datetime: datetime, tariff_code: str, rrp: float):
    return rrp / 10

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    rrp_c_kwh = rrp / 10
    tariff = tariffs.get(tariff_code)
    if not tariff:
        slope = 1.037869032618134
        intercept = 5.586606750833143
        return rrp_c_kwh * slope + intercept
    for period, start, end, rate in tariff['periods']:
        if start <= interval_time < end or (start > end and (interval_time >= start or interval_time < end)):
            return rrp_c_kwh + rate
    return rrp_c_kwh + (tariff['rate'] if isinstance(tariff['rate'], float) else list(tariff['rate'].values())[0])
