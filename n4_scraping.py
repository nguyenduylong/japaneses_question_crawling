from bs4 import BeautifulSoup
import requests
import mysql.connector

N4_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=362&jump_num={jump_num}&show_num=30&kyu=3&syu=%E8%AA%9E%E5%BD%99&target=all'
BUNPOU_N4_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=1147&jump_num={jump_num}&show_num=30&kyu=3&syu=%E6%96%87%E6%B3%95&target=all'

N2_N3_GOI_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=915&jump_num={jump_num}&show_num=30&kyu=2&syu=%E8%AA%9E%E5%BD%99&target=all'
N2_N3_BUNPOU_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=1009&jump_num={jump_num}&show_num=30&kyu=2&syu=%E6%96%87%E6%B3%95&target=all'

N1_GOI_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=462&jump_num={jump_num}&show_num=30&kyu=1&syu=%E8%AA%9E%E5%BD%99&target=all'
N1_BUNPOU_URL = 'http://www.n-lab.org/library/mondaidata/test.php?mode=html&dbupdate=0&data_count=1385&jump_num={jump_num}&show_num=30&kyu=1&syu=%E6%96%87%E6%B3%95&target=all'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

questiondb = mysql.connector.connect(host='localhost', user='root', password='', database='japanese_questions')

cursor = questiondb.cursor()

questions = []
for i in range(0, 15):
    crawl_url = N1_GOI_URL.format(jump_num=(30 * i))
    print(crawl_url)
    page = requests.get(crawl_url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_element = soup.find('table')
    tr_elements = table_element.findAll('tr')
    for tr_index in range(0, 30):
        question_index = (tr_index * 3) + 1 
        question_tr = tr_elements[question_index]
        question_tds = question_tr.findAll('td')
        # get question string
        question_td = question_tds[1]
        question_str = question_td.getText().strip()
        
        # get answer value
        answer_td = question_tds[0]
        answer_input = answer_td.find('input', {'name': 'r_ans'})
        true_answer = answer_input.get('value')

        #get all answer choices
        answer_index = (tr_index * 3) + 2
        answers_tr = tr_elements[answer_index]

        answer_tds = answers_tr.findAll('td')

        choice_1 = answer_tds[1].find('label').getText()
        choice_2 = answer_tds[2].find('label').getText()
        choice_3 = answer_tds[3].find('label').getText()
        choice_4 = answer_tds[4].find('label').getText()

        test_count_inputs = answer_tds[5].findAll('input')
        test_count = test_count_inputs[0].get('value')
        correct_count = test_count_inputs[1].get('value')
        questions.append((question_str, choice_1, choice_2, choice_3, choice_4, int(true_answer), int(test_count), int(correct_count)))

print(len(questions))
    
insert_sql = 'insert into n_lab_n1_goi (question, choice1, choice2, choice3, choice4, correct_answer, test_count, correct_count) values (%s,%s,%s,%s,%s,%s,%s,%s)'
cursor.executemany(insert_sql, questions)
questiondb.commit()

