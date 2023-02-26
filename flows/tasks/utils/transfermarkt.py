from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import get
from datetime import datetime
import json
import logging

# defined variables
transfermarkt_url = 'https://www.transfermarkt.com'
request_headers = {'user-agent': 'transfermarkt-mage'}

def soup_prettify(soup):
    print(soup.prettify())

def get_soup_attr(soup, attr):
    try:
        return soup.string if attr == 'string' else soup[attr]
    except:
        return None

def nested_find(soup, elements):
    for element, index in elements:
        try:
            soup = soup.find_all(element, recursive=False)[index]
        except:
            soup = None
            break
    return soup

def parse_transfers(html_soup, transfer_date):

    # parse to get list of transfers
    transfers_soups = html_soup\
        .find('div', class_='responsive-table')\
        .find('div', id="yw1", class_='grid-view')\
        .find('table', class_='items')

    # check if there is no list of transfer
    if not transfers_soups:
        return []

    transfers_soups = transfers_soups.find('tbody')
    transfers_soups = list(filter(lambda soup: type(soup) is Tag, transfers_soups)) # filter only bs4.element.Tag types

    # parse transfers
    transfers = []
    for transfer_soup in transfers_soups:

        # NOTE: when navigating down in bs4, some <tbody> element are missing in the soup and we're skipping them.

        # column 1
        player_id                       = get_soup_attr(nested_find(transfer_soup,[('td',0), ('table',0), ('tr',0), ('td',1),('a', 0)]), 'href').split('/')[-1]
        name                            = get_soup_attr(nested_find(transfer_soup,[('td',0), ('table',0), ('tr',0), ('td',1),('a', 0)]), 'string')
        portrait_url                    = get_soup_attr(nested_find(transfer_soup,[('td',0), ('table',0), ('tr',0), ('td',0), ('img', 0)]), 'data-src')
        position                        = get_soup_attr(nested_find(transfer_soup,[('td',0), ('table',0), ('tr',1), ('td',0)]), 'string')

        # column 2
        age                             = get_soup_attr(nested_find(transfer_soup, [('td', 1)]), 'string')

        # column 3
        nationalities = []
        for img in nested_find(transfer_soup, [('td', 2)]).find_all('img', recursive=False):
            nationalities.append({'name': img['title'], 'url': img['src']})

        # column 4
        left_club_url                   = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 0), ('td', 0), ('a', 0), ('img', 0)]),'src')
        left_club_name                  = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 0), ('td', 1), ('a', 0)]), 'string')
        left_club_name_alt              = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 0), ('td', 1), ('a', 0)]), 'title')
        left_club_league_country_url    = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 1), ('td', 0), ('img', 0)]), 'src')
        left_club_league_country_name   = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 1), ('td', 0), ('img', 0)]), 'title')
        left_club_league_name           = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 1), ('td', 0), ('a', 0)]), 'string')
        left_club_league_name_alt       = get_soup_attr(nested_find(transfer_soup, [('td', 3), ('table', 0), ('tr', 1), ('td', 0), ('a', 0)]), 'title')

        # column 5
        join_club_url                   = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 0), ('td', 0), ('a', 0), ('img', 0)]),'src')
        join_club_name                  = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 0), ('td', 1), ('a', 0)]), 'string')
        join_club_name_alt              = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 0), ('td', 1), ('a', 0)]), 'title')
        join_club_league_country_url    = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 1), ('td', 0), ('img', 0)]), 'src')
        join_club_league_country_name   = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 1), ('td', 0), ('img', 0)]), 'title')
        join_club_league_name           = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 1), ('td', 0), ('a', 0)]), 'string')
        join_club_league_name_alt       = get_soup_attr(nested_find(transfer_soup, [('td', 4), ('table', 0), ('tr', 1), ('td', 0), ('a', 0)]), 'title')

        # column 6
        market_value                    = get_soup_attr(nested_find(transfer_soup, [('td', 5)]), 'string')

        # column 7
        fee                             = get_soup_attr(nested_find(transfer_soup, [('td', 6), ('a', 0)]), 'string')
        loan_fee                        = get_soup_attr(nested_find(transfer_soup, [('td', 6), ('a', 0), ('i', 0)]), 'string')
        transfer_url                    = get_soup_attr(nested_find(transfer_soup, [('td', 6), ('a', 0)]), 'href')

        # wrap transfer into dict and enlist

        dt_transfer_date = datetime.strptime(transfer_date, '%Y-%m-%d')

        transfers.append({
            'portrait_url': portrait_url,
            'name': str(name),
            'player_id': player_id,
            'position': str(position),
            'age': age,
            'nationalities': nationalities,
            'left_club_url': left_club_url,
            'left_club_name': left_club_name,
            'left_club_name_alt': left_club_name_alt,
            'left_club_league_country_url': left_club_league_country_url,
            'left_club_league_country_name': left_club_league_country_name,
            'left_club_league_name': left_club_league_name,
            'left_club_league_name_alt': left_club_league_name_alt,
            'join_club_url': join_club_url,
            'join_club_name': join_club_name,
            'join_club_name_alt': join_club_name_alt,
            'join_club_league_country_url': join_club_league_country_url,
            'join_club_league_country_name': join_club_league_country_name,
            'join_club_league_name': join_club_league_name,
            'join_club_league_name_alt': join_club_league_name_alt,
            'market_value': market_value,
            'fee': fee,
            'loan_fee': loan_fee,
            'transfer_url': transfer_url,
            'transfer_date': transfer_date,
            'ingested_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'y': dt_transfer_date.strftime("%Y"),
            'm': dt_transfer_date.strftime("%m"),
            'd': dt_transfer_date.strftime("%d"),
        })

    return transfers

def get_transfers_by_date(date=datetime.now().strftime("%Y-%m-%d"), page_start=1, page_end=None):

    # starting parameters
    current_page = page_start
    path = f'/transfers/transfertagedetail/statistik/top/land_id_zu/0/land_id_ab/0/leihe//datum/{date}/sort//plus/1/page/{current_page}'
    next_page = True

    # get transfers
    transfers = []
    while next_page:

        # get transfer by date html string
        url = transfermarkt_url + path
        print(url)
        r = get(url, headers=request_headers)

        # html string into html_soup
        html_soup = BeautifulSoup(r.text, 'html.parser')

        # check the current_page is equal to the current web page number
        # if they're not equal, break the loop
        pagination_list_soup = html_soup.find('li', class_='tm-pagination__list-item tm-pagination__list-item--active')
        if (pagination_list_soup):
            current_web_page_number = pagination_list_soup.find('a').string
            if int(current_web_page_number) != int(current_page):
                break

        # get transfers data from html soup
        if html_soup:
            transfers = transfers + parse_transfers(html_soup, date)

        if page_end is None:

            # check for next page
            next_page_soup = html_soup.find('li', class_='tm-pagination__list-item tm-pagination__list-item--icon-next-page')
            if (next_page_soup):
                path = next_page_soup.find('a', class_='tm-pagination__link')['href']
                current_page = int(path.split('/')[-1])
            else:
                next_page = False

        else:

            current_page = current_page + 1

            # check for page_end
            if current_page > page_end:
                next_page = False
            else:
                path = f'/transfers/transfertagedetail/statistik/top/land_id_zu/0/land_id_ab/0/leihe//datum/{date}/sort//plus/1/page/{current_page}'

    return transfers