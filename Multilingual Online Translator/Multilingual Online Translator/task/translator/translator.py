import requests
import os
import sys
from collections import deque

from bs4 import BeautifulSoup


class Translator:
    """translator"""

    ALL_LANGUAGES = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
                     'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']
    path = os.getcwd()

    def __init__(self):
        self.your_language = None
        self.to_language = None
        self.word = None
        self.req_session = requests.Session()
        self.url = []
        self.lang_titles = []  # stores language names
        self.translated = deque()  # stores all translations
        self.examples = []
        self.path = None
        self.flag = True
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def start(self):
        self.your_language = sys.argv[1]
        self.to_language = sys.argv[2]
        self.word = sys.argv[3]

        self.path = os.path.join(Translator.path, f'{self.word}.txt')

        if self.to_language != 'all' and self.to_language not in Translator.ALL_LANGUAGES:
            print(f"Sorry, the program doesn't support {self.to_language}")

        elif not os.path.exists(self.path):
            self.create_url()
        else:
            self.read_the_file()

    def create_url(self):
        if self.to_language == 'all':
            for i, val in enumerate(Translator.ALL_LANGUAGES):
                if val != self.your_language:  # Don't create english-english url, etc.
                    self.url.append(f'https://context.reverso.net/translation/'
                                    f'{self.your_language}-{Translator.ALL_LANGUAGES[i]}/{self.word}')
        else:
            self.url.append(f'https://context.reverso.net/translation/'
                            f'{self.your_language}-{self.to_language}/{self.word}')
        self.get_soup()

    def get_soup(self):
        for url in self.url:
            tmp_translated = []
            tmp_examples = []
            try:
                response = self.req_session.get(url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    name_of_the_language = soup.find('div', class_='title-content').text.split()[-1]
                    self.lang_titles.append(name_of_the_language)

                    for item in soup.find_all('a', class_='dict'):
                        tmp_translated.append(item.text.strip())
                    if name_of_the_language == 'Arabic' or name_of_the_language == 'Hebrew':
                        tmp_translated.reverse()
                    self.translated.append(tmp_translated)  # why is it reversed?

                    for item in soup.find_all('div', class_=['src', 'trg']):
                        tmp_examples.append(item.text.strip())
                    tmp_examples = list(filter(None, tmp_examples))  # removes empty strings
                    self.examples.append(tmp_examples)
                else:
                    print(f'Sorry, unable to find {self.word}')
                    self.flag = False
                    break
            except requests.ConnectionError as err:
                print('Something wrong with your internet connection')
                self.flag = False
                break
        if self.flag:
            self.write_a_content()

    def write_a_content(self):
        """Prepares soup content for writing to a file. In case '0' takes one example for each language.
        Otherwise it takes 5 examples"""
        if self.to_language == 'all':
            with open(self.path, 'w') as file:
                for i in range(len(self.lang_titles)):
                    file.write(f'{self.lang_titles[i]} Translations:\n')
                    file.write(f'{self.translated[i][0]}\n\n')
                    file.write(f'{self.lang_titles[i]} Example:\n')
                    file.write(f'{self.examples[i][0]}\n')
                    file.write(f'{self.examples[i][1]}\n')
                    file.write('\n\n')
        else:
            with open(self.path, 'w') as file:
                file.write(f'{self.lang_titles[0]} Translations:\n')
                for i in range(5):
                    file.write(f'{self.translated[0][i]}\n')
                file.write('\n')

                file.write(f'{self.lang_titles[0]} Examples:\n')
                for i in range(10):
                    if i != 0 and i % 2 == 0:
                        file.write('\n')
                    file.write(f'{self.examples[0][i]}')
                    file.write('\n')
        self.read_the_file()

    def read_the_file(self):
        with open(self.path, 'r') as file:
            translation = file.read()
            print(translation)


def main():
    obj = Translator()
    obj.start()


if __name__ == '__main__':
    main()
