import time
import datetime
import codecs
import requests
import json
import sys
from lxml import html

def scrape_leaderboard(pagenum):
    players = []

    if pagenum == 1:
        url = "https://scoresaber.com/global"
    else:
        url = "https://scoresaber.com/global/{}".format(pagenum)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    rows = tree.xpath('//div/table/tbody/tr')
    with open('country-codes.json') as file:
        countrycodes = json.load(file)

    for row in rows:
        addPersonFlag = 0
        rank = row.xpath('td/text()')[2].replace(',','').strip()
        pp = row.xpath('td/span/text()')[0].replace("pp",'').replace(',','').strip()
        #Some names on ScoreSaber are not text, so this set the name to "UNREADABLE"
        try:
            name = row.xpath('td/a/span/text()')[0].replace(',','')
        except:
            name = "UNREADABLE"

        countrycode = row.xpath('td/a/img')[0].attrib['src'][15:].replace(".png",'').upper()
        if countrycode in countrycodes.keys():
            country = countrycodes[countrycode]
        else:
            country = countrycode
        if addPersonFlag == 0:
            players.append({'name': name, 'pp': pp, 'country': country, 'rank': rank})

    return players

def write_leaderboard_rankings_csv(sPage, ePage):
    dt = datetime.datetime.now()
    timestamp = "{}-{}-{}".format(dt.day,dt.month,dt.year)

    with codecs.open("leaderboard-rankings-{}.csv".format(timestamp), 'w', encoding='utf-8') as file:
        for x in range(sPage, ePage):
            try:
                print("Scraping page #{}...".format)
                players = scrape_leaderboard(x)
                #sleep so we don't throttle ourselves
                time.sleep(1)
            except Exception as e:
                print("Error scraping page #{}:\n{}\nHalting Scraping".format(x, e))
                break
            for player in players:
                playerdata = u"{},{},{},{}\n".format(player['rank'],player['name'],player['pp'],player['country'])
                file.write(playerdata)
        print("Scrape complete. pages " + str(sPage) + " to " + str(ePage))


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

if __name__ == "__main__":
    write_leaderboard_rankings_csv(int(sys.argv[1]), int(sys.argv[2]))
