import time
import datetime
import codecs
import requests
from lxml import html

#page to start on, and number of pages to scrape (50 results per page)
startpage = 1
maxpages = 1000

def scrape_leaderboard(pagenum):
    players = []

    if pagenum == 1:
        url = "https://scoresaber.com/global/"
    else:
        url = "https://scoresaber.com/global/{}".format(pagenum)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    rows = tree.xpath('//div/table/tbody/tr')

    for row in rows:
        rank = row.xpath('td/text()')[0].replace('#','').strip()
        pp = row.xpath('td/text()')[1].replace("pp",'').replace(',','').strip()
        name = row.xpath('td/a/text()')[0].replace(',','')
        country = row.xpath('td/a/img')[0].attrib['src'][15:].replace(".png",'').upper()
        players.append({'name': name, 'pp': pp, 'country': country, 'rank': rank})

    return players

def write_leaderboard_rankings_csv():
    dt = datetime.datetime.now()
    timestamp = "{}-{}-{}".format(dt.day,dt.month,dt.year)

    with codecs.open("leaderboard-rankings-{}.csv".format(timestamp), 'w', encoding='utf-8') as file:
        for x in range(startpage,maxpages+1):
            try:
                print("Scraping page #{}...".format)
                players = scrape_leaderboard(x)
                #sleep so we don't throttle ourselves
                time.sleep(2)
            except Exception as e:
                print("Error scraping page #{}:\n{}\nHalting Scraping".format(x, e))
                break
            for player in players:
                playerdata = u"{},{},{},{}\n".format(player['rank'],player['name'],player['pp'],player['country'])
                file.write(playerdata)
        print("Scrape complete. {} leaderboard pages scraped.".format(maxpages))


if __name__ == "__main__":
    write_leaderboard_rankings_csv()
