import requests
from bs4 import BeautifulSoup

def get_wikipedia_summary(title):
    url = f"https://zh.wikipedia.org/wiki/{title}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    summary_paragraphs = soup.select('div.mw-parser-output > p')
    summary_text = ' '.join([p.text for p in summary_paragraphs if p.text.strip() != ''])

    return summary_text

print(get_wikipedia_summary("广州"))