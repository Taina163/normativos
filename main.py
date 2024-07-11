import os
import re

import bs4
import requests
import json

from tqdm import tqdm


def main():
    urls = [
        'https://www.ufsm.br/pro-reitorias/proplan/resolucoes-por-ano',
        'https://www.ufsm.br/pro-reitorias/proplan/portarias-normativas-por-ano',
        'https://www.ufsm.br/pro-reitorias/proplan/instrucoes-normativas-por-ano',
        'https://www.ufsm.br/pro-reitorias/proplan/outros-emitidos-ate-2020-por-ano'
    ]

    collected = {}
    for url in urls:
        content_type = url.split('/')[-1]
        with requests.session() as sess:
            answer = sess.get(url)
            bs = bs4.BeautifulSoup(answer.text, 'html.parser')
            bs = bs.find('div', attrs={'class': 'entry-content'})
            links = bs.findAll('a')  # type: list
            last_year = None

            with tqdm(range(len(links)), desc=f'Coletando links de {content_type}') as pbar:
                for link in links:  # type: bs4.Tag
                    # é um ano
                    if ('class' in link.attrs) and ('elementor-toggle-title' in link.attrs['class']):
                        last_year = int(re.search('[0-9]{4}', link.text)[0])
                        collected[last_year] = []
                    else:
                        link = link.attrs['href']

                        collected[last_year] += [link]
                    pbar.update(1)

        with open(os.path.join('instance', 'data', content_type + '.json'), 'w', encoding='utf-8') as write_file:
            json.dump(collected, write_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
