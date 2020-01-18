import sys
import re

from datetime import date
from termcolor import cprint, colored

daysKey = 'days'
timeKey = 'time'
monthsKey = 'months'
subsKey = 'subs'
totalsKey = 'total'
deetsKey = 'deets'

def newCounter(habit):
    counter = {'total': 0, daysKey: {}, monthsKey: {}, timeKey: {}, subsKey: {}, deetsKey: {}}

    if habit === 'EX':
        counter[deetsKey] = {
            miles: 0,
            time: 0,
            avg: 0
        }

    return counter

def cleanDay(day):
    day = day.lower()
    if (day in ['weds', 'wed.', 'mid-day']):
        return 'wed'

    if(day in ['sunday', 'sun.']):
        return 'sun'
    
    return day;

def getTimeOfDay(time):
    t = time.lower()
    hour = None

    if t.find(':') > -1:
        hour = int(t.split(':')[0])

    if t in ['morning', 'early', '5;30', '7am'] or (hour > 4 and hour <= 9):
        return 'morning'

    elif t in ['mid-day', 'mid day', 'mid'] or (hour > 9 and hour <= 12):
        return 'mid-day'

    elif t in ['afternoon', 'afternoom'] or (hour > 12 and hour <= 16):
        return 'afternoon'

    elif t == 'evening' or (hour > 16 and hour <= 19):
        return 'evening'

    elif t in ['night', '22'] or (hour > 19 and hour <= 22):
        return 'night'
    
    elif t == 'late' or (hour > 22 and hour <= 23) or (hour >= 0 and hour <= 4):
        return 'late-night'

    else:
        return 'unknown-' + t

def header(title):
    cprint(("\n" + title).upper(), 'red')

def debug(msg):
    cprint(msg, 'yellow')

filename = './habits-2020.csv'
debug("reading the file '" + filename + "'")

file = open(filename, 'r')
lines = file.readlines()

onFirstLine = True;
counts = {}

start = date(2020, 1, 1)
end = date.today()
diff = end - start
daysSoFar = diff.days
totalRecords = 0
totalMiles = 0
totalRuns = 0
milesRegex = re.compile('\d+\.?(\d+)?')

for line in lines:
    if onFirstLine:
        onFirstLine = False
        continue

    parts = line.split(',')
    date = parts[0]
    dayAndTime = parts[1]
    habit = parts[2].strip()
    sub = parts[3].strip()
    notes2 = parts[4].strip()
    notes3 = parts[5].strip()
    notes4 = parts[6].strip()
    
    dayAndTimeParts = dayAndTime.split(' ');
    day = cleanDay(dayAndTimeParts[0])
    time = dayAndTimeParts[1]

    dateParts = date.split('/')
    month = dateParts[0]
    totalRecords += 1
    # print "DATE: ", parts[0], " DAY/TIME: ", parts[1], " THING: ", parts[2], " NOTES: ", parts[3]
    
    if habit not in counts:
        counts[habit] = newCounter(habit)

    if habit != 'S':
        if sub not in counts[habit][subsKey]:
            counts[habit][subsKey][sub] = {totalsKey: 0};

        counts[habit][subsKey][sub][totalsKey] += 1

    if sub in ['RUN-IN', 'RUN-OUT']
        counts[habit][deetsKey]['miles'] += notes2
        counts[habit][deetsKey]['time'] += notes3

    counts[habit][totalsKey] += 1

    if (day not in counts[habit][daysKey]):
        counts[habit][daysKey][day] = 0
        
    counts[habit][daysKey][day] += 1

    if (month not in counts[habit]['months']):
        counts[habit][monthsKey][month] = 0

    counts[habit][monthsKey][month] += 1

    timeOfDay = getTimeOfDay(time)

    if (timeOfDay not in counts[habit][timeKey]):
        counts[habit][timeKey][timeOfDay] = 0;

    counts[habit][timeKey][timeOfDay] += 1

prettyMonths = {
    1: 'jan',
    2: 'feb',
    3: 'mar',
    4: 'apr',
    5: 'may',
    6: 'jun',
    7: 'jul',
    8: 'aug',
    9: 'sep',
    10: 'oct',
    11: 'nov',
    12: 'dec'
}

days = [
    'mon',
    'tues',
    'wed',
    'thurs',
    'fri',
    'sat',
    'sun'
]

delim = "   "
separator = ":"

for habit in counts:
    # HEADER
    avg = round((daysSoFar * 1.0)/counts[habit][totalsKey], 2)
    cprint("\n\n" + delim + habit + separator + " You have done this " + str(counts[habit]['total']) + " times this year. That's once every " + str(avg) + " days.\n", 'grey', 'on_white', attrs=['bold'])

    # TIME OF DAY
    header('time of day')

    for tod in ['morning', 'mid-day', 'afternoon', 'night', 'late-night']:
        todCount = 0
        if tod in counts[habit][timeKey]:
            todCount = counts[habit][timeKey][tod]

        print tod + separator, todCount


    # DAY
    header('days')

    for day in days:
        dayCount = 0
        if day in counts[habit][daysKey]:
            dayCount = counts[habit][daysKey][day]

        print day + separator, dayCount

    # MONTH
    header('months')

    for monthNum in range(1,13):
        monthCount = 0
        if (str(monthNum) in counts[habit][monthsKey]):
            monthCount = counts[habit][monthsKey][str(monthNum)]

        print prettyMonths[monthNum] + separator, monthCount

    # SUBS
    header('subs')

    for sub in counts[habit][subsKey]:
        print sub + ': ' + str(counts[habit][subsKey][sub][totalsKey])

debug("total days in year" + separator + " " + str(daysSoFar))
debug("file parsed" + separator + " " + filename + "\n")
