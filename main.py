import json
from dateutil import rrule
from datetime import datetime
from dateutil.parser import parse


def hour_per_day(in_locations):
    # make them pretty
    day_locations = []
    for loc in in_locations:
        location = {
            'latitude': loc['latitudeE7'],
            'longitude': loc['longitudeE7'],
            'timestamp': int(loc['timestampMs']),
            'date': get_readable_date_from_ms(loc['timestampMs'])
        }
        day_locations.append(location)

    list_len = len(day_locations)
    time_at_location = []
    for i in range(0, list_len):
        lat = abs(day_locations[i]['latitude'] - 413851990)
        lon = abs(day_locations[i]['longitude'] - 21429410)
        if lat + lon < 50000:
            time_at_location.append({
                'timestamp': day_locations[i]['timestamp'],
                'date': day_locations[i]['date']
            })
    if len(time_at_location) > 0:
        return (time_at_location[0]['timestamp'] - time_at_location[len(time_at_location)-1]['timestamp']) / 60.0 / 60.0 / 1000.0 - 1.0
    else:
        return 0


def get_readable_date_from_ms(timestamp_ms):
    timestamp = int(timestamp_ms) / 1000.0
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


# read data
j_file = './data/1483225200000.json'
with open(j_file) as train_file:
    dict_train = json.load(train_file)

locations = dict_train

# get weekly breakdown
now = parse("2017-01-01T00:00:00-00:00")
then = parse("2018-01-01T00:00:00-00:00")
weeks = []
for dt in rrule.rrule(rrule.WEEKLY, dtstart=now, until=then):
    weeks.append(int(dt.strftime('%s')))

for w in range(0, len(weeks)-1):
    in_week = 0
    # get daily breakdown
    first = datetime.fromtimestamp(weeks[w])
    last = datetime.fromtimestamp(weeks[w+1])
    days = []
    for dt in rrule.rrule(rrule.DAILY, dtstart=first, until=last):
        days.append(int(dt.strftime('%s')) * 1000)

    for d in range(0, len(days) - 1):
        # get locations for a day
        locations_list = []
        for value in locations:
            if days[d] <= int(value['timestampMs']) <= days[d + 1]:
                locations_list.append(value)

        # get hours for that day
        in_week += hour_per_day(locations_list)

    print in_week
