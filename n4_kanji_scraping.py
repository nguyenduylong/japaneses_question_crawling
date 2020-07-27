from bs4 import BeautifulSoup
import requests
import mysql.connector

N4_URL = 'https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n4-kanji-exercise-2/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


questions = []
crawl_url = N4_URL

with open('n4_kanji.csv','a') as file:
    page = requests.get(crawl_url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    form_element = soup.find('form')
    # if form_element is None:
    #     return False
    question_elements = form_element.findAll('p')
    # if len(question_elements) == 0 :
    #     return False
    for element in question_elements:
        editted_QAs = []
        question_answers = element.getText().split('\n')
        for text in question_answers:
            if text is None or text == '':
                continue
            editted_QAs.append(text.strip())
        if len(editted_QAs) == 5:
            question = editted_QAs[0]
            editted_QAs[0] = question[(question.find('.') + 1):].strip()
            QA_string = ', '.join(editted_QAs) + ',  , '
            file.write(QA_string)
            file.write('\n')
