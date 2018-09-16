import requests
import os
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


if os.path.isfile(os.getcwd() + '/match.json'):
    os.remove(os.getcwd() + '/match.json')
else:
    pass

def get_source(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

"""
Get all the upcoming matches
@param number_days : get the upcoming matches for the number of following days. 

@return: a panda dataframe with all the matches information. 
"""
def upcomingmatches(number_days=0):
    matchlinks_um = []
    today = datetime.today()

    for i in range(number_days + 1):

        matchlinks = []
        matchdates = []
        matchclocks = []
        matcheventnames = []
        teamlogos = []
        matchbestof = []
        matchstatus = []
        teamnames1 = []
        teamnames2 = []
        match = {'matches': []}
        
        soup = get_source('https://hltv.org/matches')
        
        if soup.find(class_="standard-headline", text=(str(today)[:10])) is None:
            print("No upcoming matches today", (str(today)[:10]))
            today += timedelta(days=1)
            continue
        else:
            print("Upcoming matches on date", (str(today)[:10]))

        for links in soup.find(class_="standard-headline", text=(str(today)[:10])).find_parent().find_all(
                class_="upcoming-match"):
            matchlinks_um.append('https://hltv.org' + links.get('href'))
            matchlinks.append('https://hltv.org' + links.get('href'))
        for x in tqdm(range(len(matchlinks_um))):
            soup = get_source(matchlinks_um[x])
            time_class = soup.find('div', class_='time')['data-unix']
            realtimeclock = datetime.fromtimestamp(int(time_class[:10])).time()
            if realtimeclock != '00:00:00':
                matchclocks.append(realtimeclock)
            tn = soup.find_all('div', class_='teamName')
            teamnames1.append(tn[0].text)
            teamnames2.append(tn[1].text)
            matchdate = soup.find('div', class_='date').text
            matchdates.append(matchdate)
            eventname = soup.find('div', class_='event text-ellipsis').text
            matcheventnames.append(eventname)
            for lg in soup.find_all('img', class_='logo'):
                teamlogos.append(lg.get('src'))
            maps = soup.find('div', class_='standard-box veto-box').find(class_='padding preformatted-text').text
            if maps.startswith('Best'):
                matchbestof.append(maps[:9])
            else:
                matchbestof.append(maps[:12])
            matchstatus.append('UPCOMING')
            time.sleep(0.01)
        today += timedelta(days=1)

    all_data = []

    for ml, mc, tm1, tm2, md, me, mb in zip(matchlinks, matchclocks, teamnames1, teamnames2, matchdates, matcheventnames, matchbestof):
        all_data.append([ml, mc, tm1, tm2, md, me, mb])

    dataframe = pd.DataFrame(all_data, \
            columns=["match_links", "match_clocks", "teamnames1", "teamnames2", "matchdates", "matcheventnames", "matchbestof"])

    return dataframe

def livematches():
    matchlinks_lm = []
    soup = get_source('https://hltv.org/matches')
    control = soup.find(class_='live-matches')
    if control is not None:
        for links in soup.find(class_='live-matches').find_all('a'):
            matchlinks_lm.append('https://hltv.org' + links.get('href'))
            matchlinks.append('https://hltv.org' + links.get('href'))
        for x in tqdm(range(len(matchlinks_lm))):
            soup = get_source(matchlinks_lm[x])
            time_class = soup.find('div', class_='time')['data-unix']
            realtimeclock = datetime.fromtimestamp(int(time_class[:10])).time()
            matchclocks.append(realtimeclock)
            for tn in soup.find_all('div', class_='teamName'):
                teamnames.append(tn.text)
            matchdate = soup.find('div', class_='date').text
            matchdates.append(matchdate)
            eventname = soup.find('div', class_='event text-ellipsis').text
            matcheventnames.append(eventname)
            for lg in soup.find_all('img', class_='logo'):
                teamlogos.append(lg.get('src'))
            maps = soup.find('div', class_='standard-box veto-box').find(class_='padding preformatted-text')
            if maps is not None:
                maps = maps.text
                if maps.startswith('Best'):
                    matchbestof.append(maps[:9])
                else:
                    matchbestof.append(maps[:12])
            matchstatus.append('LIVE')
            time.sleep(0.01)
    return len(matchlinks_lm)

"""
Get all the results from HLTV
"""
def results():

    matchlinks = []
    matchdates = []
    matchclocks = []
    matcheventnames = []
    teamlogos = []
    matchbestof = []
    matchstatus = []
    teamnames1 = []
    teamnames2 = []

    matchlinks_rs = []
    soup = get_source('https://hltv.org/results')
    now = datetime.now()
    month = datetime.strftime(now, '%B')
    today = datetime.strftime(now, '%d')
    yesterday = datetime.strftime(now + timedelta(-1), '%d')
    year = datetime.strftime(now, '%Y')
    check = [month, today, year]
    resultdates = []

    for tddate in soup.find_all(class_='standard-headline'):
        headline = str(tddate.text).split()
        if len(headline) != 5:
            continue
        mnth = headline[2]
        tdy = headline[3][:-2]
        yr = headline[4]
        checkmdl = [mnth, tdy, yr]
        if check == checkmdl:
            resultdates.append(tddate.text)
            break
        else:
            continue
    for yddate in soup.find_all(class_='standard-headline'):
        check = [month, yesterday, year]
        headline = str(yddate.text).split()
        if len(headline) != 5:
            continue
        mnth = headline[2]
        ydy = headline[3][:-2]
        yr = headline[4]
        checkmdl = [mnth, ydy, yr]
        if check == checkmdl:
            resultdates.append(yddate.text)
            break
        else:
            continue
    for nm in range(len(resultdates)):
        for links in soup.find(class_='standard-headline', text=(resultdates[nm])).find_parent().find_all(
                class_='a-reset'):
            matchlinks_rs.append('https://hltv.org' + links.get('href'))
            matchlinks.append('https://hltv.org' + links.get('href'))
    for x in tqdm(range(len(matchlinks_rs))):
        soup = get_source(matchlinks_rs[x])
        time_class = soup.find('div', class_='time')['data-unix']
        realtimeclock = datetime.fromtimestamp(int(time_class[:10])).time()
        matchclocks.append(realtimeclock)
        for tn in soup.find_all('div', class_='teamName'):
            teamnames.append(tn.text)
        matchdate = soup.find('div', class_='date').text
        matchdates.append(matchdate)
        eventname = soup.find('div', class_='event text-ellipsis').text
        matcheventnames.append(eventname)
        for lg in soup.find_all('img', class_='logo'):
            teamlogos.append(lg.get('src'))
        maps = soup.find('div', class_='standard-box veto-box').find(class_='padding preformatted-text').text
        if maps.startswith('Best'):
            matchbestof.append(maps[:9])
        else:
            matchbestof.append(maps[:12])
        matchstatus.append('FINISHED')
        time.sleep(0.01)

def get_all_results():
    print('Upcoming matches are getting pulled.')
    upcomingmatches()
    time.sleep(1)
    print('Live matches are getting pulled.')
    livematches()
    time.sleep(1)
    print('Results are getting pulled.')
    results()
    time.sleep(1)
    print('Matches are being written.')
    time.sleep(1)


    teamA = teamnames[0::2]
    teamB = teamnames[1::2]
    for n in range(len(matchlinks)):
        print(teamA[n], 'vs', teamB[n], 'on', matchdates[n], 'at', matcheventnames[n], matchclocks[n], matchstatus[n])

    teamAlogo = teamlogos[0::2]
    teamBlogo = teamlogos[1::2]


    for dn in range(len(matchlinks)):

        match['matches'].append({
            'team1': str(teamA[dn]),
            'team2': str(teamB[dn]),
            'eventname': str(matcheventnames[dn]),
            'date': str(matchdates[dn]),
            'clock': str(matchclocks[dn]),
            'bo': str(matchbestof[dn]),
            'status': str(matchstatus[dn]),
            'team1logo': str(teamAlogo[dn]),
            'team2logo': str(teamBlogo[dn])
        })


    dump = json.dumps(match, indent=2)
    with open(os.getcwd() + '/match.json', 'a') as f:
        f.write(dump)
