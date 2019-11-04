#!/usr/bin/env python
import json
import os

import bs4
import requests
import argument


def fetch_actor_info(actor_id):
    html = requests.get(f'https://www.imdb.com/name/{actor_id}/mediaindex').text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    name = soup.title.text.split('on IMDb', 1)[0]
    media = [
        (a['title'], a.img['src']) for a in soup.find_all('a') if a['href'].startswith(f'/name/{actor_id}/mediaviewer')
    ]
    return {'name': name, 'media': media}


@argument.entrypoint
def main(*, count_json: str = 'counts.json', res_json: str = 'res.json'):
    """Fetch the actor media pages for actors mentioned in count_json.

    Args:
        count_json: list of actor_id, counts
        res_json: resulting json document containing name and media
    """

    counts = json.load(open(count_json))
    if os.path.isfile(res_json):
        res = json.load(open(res_json))
    else:
        res = {}

    for idx, (actor_id, _) in enumerate(counts):
        if not actor_id in res:
            res[actor_id] = fetch_actor_info(actor_id)
        elif idx % 100 == 0:
            print(idx)
            with open(res_json, 'w') as fout:
                json.dump(res, fout)


if __name__ == '__main__':
    main()
