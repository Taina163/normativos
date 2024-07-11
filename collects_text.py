import bs4
import nltk
import requests
from nltk.corpus import stopwords
import json
import argparse


def main(json_path):
    nltk.download('stopwords')
    language = "portuguese"

    with open(json_path, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)

    for year, urls in data.items():
        for url in urls:
            with requests.session() as sess:
                answer = sess.get(url)
                bs = bs4.BeautifulSoup(answer.text)
                bs = bs.find('div', attrs={'class': 'main-section'})

                title = bs.find('h1', attrs={'class': 'entry-title'}).text

    # for word in stopwords.words(language):
    #     print(word)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Descrição do script.'
    )

    parser.add_argument(
        '--json-path', action='store', required=True,
        help='Link para um arquivo json com os links das informações a serem coletadas.'
    )

    args = parser.parse_args()
    main(args.json_path)
