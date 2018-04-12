import json
import os
import shutil
from dateutil import rrule
from datetime import datetime
from dateutil.parser import parse

# read data
j_file = 'data.json'
with open(j_file) as train_file:
    dict_train = json.load(train_file)

locations = dict_train['locations']

# create dir for new data
dir = './data'
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)

# get range of years
firstYear = datetime.fromtimestamp(int(locations[len(locations)-1]['timestampMs'])/1000).year
lastYear = datetime.fromtimestamp(int(locations[0]['timestampMs'])/1000).year

start = parse(str(firstYear) + "-01-01T00:00:00-00:00")
end = parse(str(lastYear + 1) + "-01-01T00:00:00-00:00")
years = []
for dt in rrule.rrule(rrule.YEARLY, dtstart=start, until=end):
    years.append(int(dt.strftime('%s')) * 1000)

# beak data into separate files
for y in range(0, len(years)-1):
    locations_list = []
    for value in locations:
        if years[y] <= int(value['timestampMs']) <= years[y + 1]:
            locations_list.append(value)
    with open('./data/' + str(years[y]) + '.json', 'w') as fp:
        json.dump(locations_list, fp)
