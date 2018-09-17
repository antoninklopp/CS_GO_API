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

    for _ in range(number_days + 1):

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

def results(number_days=1): 
    """
    Get all the results from HLTV

    @param number_days : get the results from the n last days. 
    """
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

    print(number_days)
    number_results = 0
    page_number = 0

    while number_days > number_results:
        
        resultdates = []

        if page_number != 0:
            soup = get_source('https://hltv.org/results' + "?offset=" + str(page_number) + "00")

        now = datetime.now() - timedelta(days=number_results-1)
        for _ in range(number_results, number_days + 2, 1):
            month = datetime.strftime(now, '%B')
            today = datetime.strftime(now, '%d')
            year = datetime.strftime(now, '%Y')
            check = [month, today, year]
            for tddate in soup.find_all(class_='standard-headline'):
                headline = str(tddate.text).split()
                if len(headline) != 5:
                    continue
                mnth = headline[2]
                tdy = headline[3][:-2]
                yr = headline[4]
                checkmdl = [mnth, tdy, yr]
                if (check[0] == checkmdl[0]) and (int(check[1]) == int(checkmdl[1])) and (int(check[1]) == int(checkmdl[1])):
                    resultdates.append(tddate.text)
                    number_results += 1
                    break
                else:
                    # print(tddate.text)
                    continue

            now -= timedelta(days=1)

        print(number_results, number_days)

        print("number results", number_results)
        
        for nm in range(len(resultdates)):
            for links in soup.find(class_='standard-headline', text=(resultdates[nm])).find_parent().find_all(
                    class_='a-reset'):
                matchlinks_rs.append('https://hltv.org' + links.get('href'))
                matchlinks.append('https://hltv.org' + links.get('href'))
        for x in tqdm(range(page_number * 100, len(matchlinks_rs))):
            soup_match = get_source(matchlinks_rs[x])
            time_class = soup_match.find('div', class_='time')['data-unix']
            realtimeclock = datetime.fromtimestamp(int(time_class[:10])).time()
            matchclocks.append(realtimeclock)
            tn = soup_match.find_all('div', class_='teamName')
            teamnames1.append(tn[0].text)
            teamnames2.append(tn[1].text)
            matchdate = soup_match.find('div', class_='date').text
            matchdates.append(matchdate)
            eventname = soup_match.find('div', class_='event text-ellipsis').text
            matcheventnames.append(eventname)
            for lg in soup_match.find_all('img', class_='logo'):
                teamlogos.append(lg.get('src'))
            maps = soup_match.find('div', class_='standard-box veto-box').find(class_='padding preformatted-text').text
            if maps.startswith('Best'):
                matchbestof.append(maps[:9])
            else:
                matchbestof.append(maps[:12])
            matchstatus.append('FINISHED')
            time.sleep(0.01)
            

        page_number += 1

    all_data = []

    for ml, mc, tm1, tm2, md, me, mb in zip(matchlinks, matchclocks, teamnames1, teamnames2, matchdates, matcheventnames, matchbestof):
        all_data.append([ml, mc, tm1, tm2, md, me, mb])

    dataframe = pd.DataFrame(all_data, \
            columns=["match_links", "match_clocks", "teamnames1", "teamnames2", "matchdates", "matcheventnames", "matchbestof"])

    return dataframe