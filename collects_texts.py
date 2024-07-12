import os
import re
from functools import reduce

import bs4
import nltk
import requests
from nltk.corpus import stopwords
import json
import argparse
from tqdm import tqdm
import operator as op
import itertools as it


def main(json_path):
    nltk.download('stopwords', download_dir=os.path.join('instance', 'nltk_data'))
    language = "portuguese"

    _path_docs = os.path.join(os.path.dirname(json_path), 'docs')
    if not os.path.exists(_path_docs):
        os.mkdir(_path_docs)
    _files = os.listdir(_path_docs)

    _files = [x for x in os.listdir(json_path) if '.json' in x]

    data = dict()
    for _file in _files:
        with open(os.path.join(json_path, _file), 'r', encoding='utf-8') as read_file:
            _read = json.load(read_file)
            for k, v in _read.items():
                try:
                    data[k].extend(v)
                except KeyError:
                    data[k] = v

    _tuples = []
    for k, v in data.items():
        _tuples.extend(list(zip(it.repeat(k, len(v)), v)))

    urls = list(zip(*_tuples))[-1]

    for year, url in tqdm(_tuples, desc='Processando documentos'):
        filename = url[url.rfind('/') + 1:] + '.html'

        if filename not in _files:
            with (requests.session() as sess,
                  open(os.path.join(_path_docs, filename), 'w', encoding='utf-8') as write_file):
                contents = sess.get(url).text
                write_file.write(contents)
        else:
            with open(os.path.join(_path_docs, filename), 'r', encoding='utf-8') as read_file:
                contents = read_file.read()

        bs = bs4.BeautifulSoup(contents, features='html.parser')
        title = bs.find('h1', attrs={'class': 'entry-title'}).text
        body = bs.find('div', attrs={'class': 'entry-content'})

        refs = bs.findAll('a')
        # um link válido é um que linka para outra normativa da ufsm
        # TODO search não está funcionando direito!
        # https://www.ufsm.br/pro-reitorias/proplan/resolucao-n-037-2010
        valid_refs = [x for x in refs if ('href' in x.attrs) and (x.attrs['href'] in urls)]
        z = 0


    # for word in stopwords.words(language):
    #     print(word)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Descrição do script.'
    )

    parser.add_argument(
        '--json-path', action='store', required=True,
        help='Link para uma pasta com arquivos json com os links das informações a serem coletadas.'
    )

    args = parser.parse_args()
    main(args.json_path)
