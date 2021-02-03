import requests
from bs4 import BeautifulSoup
import sys

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
             'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian',
             'Turkish']


def translate(from_lang, to_lang, word):
    language_pair = f'{from_lang.lower()}-{to_lang.lower()}'
    url = f'http://context.reverso.net/translation/{language_pair}/{word}'

    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if r:
        soup = BeautifulSoup(r.content, 'html.parser')
        word_div = soup.find('div', {'id': 'translations-content'})

        word_list = []
        for word in word_div.find_all('a', limit=5):
            word_list.append(word.text.strip())

        sentence_section = soup.find('section', {'id': 'examples-content'})
        sentence_list = []
        for sentence in sentence_section.find_all('span', {'class': 'text'}, limit=10):
            sentence_list.append(sentence.text.strip())

        translates = []
        print(f'\n{to_lang} Translations:')
        translates.append(f'\n{to_lang} Translations:\n')
        print("\n".join(word_list))
        translates.append("\n".join(word_list))
        translates.append("\n")

        print(f'\n{to_lang} Examples:')
        translates.append(f'\n{to_lang} Examples:\n')
        for i in range(0, len(sentence_list) - 1, 2):
            print(sentence_list[i])
            translates.append(sentence_list[i] + "\n")
            print(sentence_list[i + 1])
            translates.append(sentence_list[i + 1] + "\n")
            print()
            translates.append("\n")

        return translates

    else:
        if "Translation into" in str(r.content):
            return f"Sorry, unable to find {word}"
        else:
            return "Something wrong with your internet connection"


args = sys.argv
if len(args) != 4:
    raise Exception("Invalid arguments")

from_lang = args[1].capitalize()
to_lang = args[2].capitalize()
word = args[3]

if from_lang not in languages and from_lang != "All":
    print(f"Sorry, the program doesn't support {from_lang}")
elif to_lang not in languages and to_lang != "All":
    print(f"Sorry, the program doesn't support {to_lang}")
else:
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        lines = []
        if to_lang == "All":
            for i in range(len(languages)):
                if languages[i] != from_lang:
                    result = translate(from_lang, languages[i], word)
                    if type(result) == str:
                        print(result)
                        break
                    else:
                        lines.extend(result)
        else:
            lines = translate(from_lang, to_lang, word)
            if type(lines) == str:
                print(lines)

        f.writelines(lines)
