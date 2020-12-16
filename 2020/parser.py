import sys
import re
import math

from datetime import date
from datetime import datetime
from termcolor import cprint, colored

daysKey = 'days'
timeKey = 'time'
monthsKey = 'months'
subsKey = 'subs'
totalsKey = 'total'
deetsKey = 'deets'

def calcTime(totalSecs):
    hours = totalSecs/3600
    mins = (totalSecs - (hours * 3600))/60
    secs = totalSecs - (hours * 3600) - (mins * 60)
    return ' A Total of: ' + str(hours) + 'h ' + str(mins) + 'm ' + str(secs) + 's (' + str(totalSecs) + ' total seconds)'

def newCounter(habit):
    counter = {'total': 0, daysKey: {}, monthsKey: {}, timeKey: {}, subsKey: {}, deetsKey: {}}

    if habit == 'EX':
        counter[deetsKey] = {
            'runs': {
                'total': 0,
                timeKey: 0,
                'miles': 0,
                'avg-miles-per-run': 0,
                'avg-mile': 0
            },
            'training': {
                'total': 0,
                timeKey: 0,
                'push-ups': 0,
                'crunches': 0,
                'lunges': 0,
                'planks': 0,
                'chin-ups': 0,
                'curls': 0,
                'shoulder-presses': 0,
                'floor-presses': 0,
            }
        }
    elif habit == 'EAT':
      counter[deetsKey] = {'cost': 0, 'avg': 0, 'avg-per-month': 0}

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

filename = './habits.csv'
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
intxTypeRegex = re.compile('^(\d)(.+)?')
timedExercises = []

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

    counts[habit][totalsKey] += 1

    if habit != 'S':
        if sub not in counts[habit][subsKey]:
            counts[habit][subsKey][sub] = {totalsKey: 0};

        counts[habit][subsKey][sub][totalsKey] += 1

    if habit == 'EAT':
        counts[habit][deetsKey]['cost'] += int(notes3)
        counts[habit][deetsKey]['avg'] = round(counts[habit][deetsKey]['cost']/counts[habit][totalsKey], 2)
        if sub not in counts[habit][deetsKey]:
            counts[habit][deetsKey][sub] = 0

        counts[habit][deetsKey][sub] += 1

    if habit == 'INTX':
        split = notes2.split('/');
        for intxType in split:
            matches = intxTypeRegex.match(intxType)
            if matches != None:
                num = int(matches.group(1))
                substance = matches.group(2)

                if substance not in counts[habit][deetsKey]:
                  counts[habit][deetsKey][substance] = 0

                counts[habit][deetsKey][substance] += num

    if sub in ['RUN-IN', 'RUN-OUT']:
        matches = milesRegex.match(notes2)

        if matches != None:
            split = notes3.split(':')
            hours = int(split[0])
            mins = int(split[1])
            secs = int(split[2])
            counts[habit][deetsKey]['runs']['total'] += 1
            counts[habit][deetsKey]['runs'][timeKey] += (hours * 360) + (mins * 60) + secs
            counts[habit][deetsKey]['runs']['miles'] += float(matches.group())

            secondsPerMile = float(counts[habit][deetsKey]['runs'][timeKey])/float(counts[habit][deetsKey]['runs']['miles'])
            minsPerMile = round(secondsPerMile/float(60), 2)
            avgMileSplit = str(minsPerMile).split('.')
            wholeMinsPerMile = avgMileSplit[0]
            wholeSecondsPerMile = str(int(math.ceil(float('.' + avgMileSplit[1]) * 60))).zfill(2)
            counts[habit][deetsKey]['runs']['avg-mile'] =  wholeMinsPerMile + ':' + wholeSecondsPerMile # str(wholeMins) + ':' + str(partMins * 60)
            
            avgMilesPerRun = float(counts[habit][deetsKey]['runs']['miles'])/float(counts[habit][deetsKey]['runs']['total'])
            counts[habit][deetsKey]['runs']['avg-miles-per-run'] = round(avgMilesPerRun, 2) # str(wholeMins) + ':' + str(partMins * 60)

    if sub == 'ST':
        counts[habit][deetsKey]['training']['total'] += 1;
        counts[habit][deetsKey]['training'][timeKey] += int(notes3.split('min')[0]) * 60
        exercises = notes2.split('/')

        if len(exercises) > 1:
            counts[habit][deetsKey]['training']['crunches'] += int(exercises[0])
            counts[habit][deetsKey]['training']['push-ups'] += int(exercises[1])
            counts[habit][deetsKey]['training']['lunges'] += int(exercises[2].split(' ')[0])

            for i in range(3, len(exercises)):
                spl = exercises[i].split(' ')
                repsOrMinsSplit = spl[0].split('min')
                repsOrMins = int(repsOrMinsSplit[0])
                exerciseKey = spl[1]

                isTime = len(repsOrMinsSplit) > 1

                if isTime: 
                    timedExercises.append(exerciseKey)

                if exerciseKey not in counts[habit][deetsKey]['training']:
                    counts[habit][deetsKey]['training'][exerciseKey] = 0

                counts[habit][deetsKey]['training'][exerciseKey] += repsOrMins

    if habit == 'S':
        if timeKey not in counts[habit][deetsKey]:
            counts[habit][deetsKey][timeKey] = 0

        counts[habit][deetsKey][timeKey] += int(sub.split('min')[0]) * 60
        

    if habit == 'M':
        if timeKey not in counts[habit][deetsKey]:
            counts[habit][deetsKey][timeKey] = 0

        counts[habit][deetsKey][timeKey] += int(notes2.split('min')[0]) * 60

        if sub == 'PRN':
            if notes3 not in counts[habit][deetsKey]:
                counts[habit][deetsKey][notes3] = 0

            counts[habit][deetsKey][notes3] += 1

    if day not in counts[habit][daysKey]:
        counts[habit][daysKey][day] = 0
        
    counts[habit][daysKey][day] += 1

    if month not in counts[habit]['months']:
        counts[habit][monthsKey][month] = 0

    counts[habit][monthsKey][month] += 1

    timeOfDay = getTimeOfDay(time)

    if timeOfDay not in counts[habit][timeKey]:
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

# calc avg spent on eating out per month
counts['EAT'][deetsKey]['avg-per-month'] = counts['EAT'][deetsKey]['cost']/datetime.today().month;

for habit in counts:
    # HEADER
    avg = round((daysSoFar * 1.0)/counts[habit][totalsKey], 2)
    isEx = habit == 'EX'
    totalTimeSpent = ''

    if timeKey in counts[habit][deetsKey] or isEx:
        if isEx:
            totalSecs = counts[habit][deetsKey]['training'][timeKey] + counts[habit][deetsKey]['runs'][timeKey]
        else: 
            totalSecs = counts[habit][deetsKey][timeKey]

        totalTimeSpent = calcTime(totalSecs)

    cprint("\n\n" + delim + habit + separator + " You have done this " + str(counts[habit]['total']) + " times this year. That's once every " + str(avg) + " days." + totalTimeSpent + "\n", 'grey', 'on_white', attrs=['bold'])

    # SUBS
    header('subs')

    for sub in counts[habit][subsKey]:
        print sub + ': ' + str(counts[habit][subsKey][sub][totalsKey])

    # DEETS
    header('deets')

    for deet in counts[habit][deetsKey]:
        if deet == timeKey: 
            continue;
            
        if deet in ['runs', 'training']:
            print "\n" + deet + ': ' + str(counts[habit][deetsKey][deet]['total'])
            for subDeet in sorted(counts[habit][deetsKey][deet]):
                if subDeet in ['total', timeKey]: 
                    continue;
                suffix = ''
                if subDeet in timedExercises:
                    suffix = ' mins'
                print '>>> ' + subDeet + ': ' + str(counts[habit][deetsKey][deet][subDeet]) + suffix
        else:
            print deet + ': ' + str(counts[habit][deetsKey][deet])

    # TIME OF DAY
    header('time of day')

    for tod in ['morning', 'mid-day', 'afternoon', 'evening', 'night', 'late-night']:
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

debug("total days in year" + separator + " " + str(daysSoFar))
debug("file parsed" + separator + " " + filename + "\n")
