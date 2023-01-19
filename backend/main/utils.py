from datetime import datetime

def format_minutes(minutes):
    hours = minutes // 60
    minutes = minutes % 60

    return f'{hours:02}:{minutes:02}'

def parse_time(time):
    try:
        return datetime.strptime(time, '%H:%M')
    except:
        return None

def validate_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        raise ValueError('date must be in YYYY-MM-DD format')
