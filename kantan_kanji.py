import requests
import json
from bs4 import BeautifulSoup
import time

url = 'https://kantan.vn/postrequest.ashx'

headers= {'content-type': "application/x-www-form-urlencoded", "accept": "*/*"}

data = {
    'm': 'dictionary',
    'fn': 'kanji_detail',
}

column_title_map = {
    'ý nghĩa': 'mean',
    'giải thích': 'explain',
    'onyomi': 'onyomi',
    'kunyomi': 'kunyomi',
    'hình ảnh gợi nhớ': 'memorable_img',
    'cách ghi nhớ': 'remember_trick',
    'trình độ': 'level',
    'số nét': 'stroke_count',
    'bộ phận cấu thành': 'constructs',
    'ví dụ': 'examples'
}

def fromLabelToColumnTitle(label):
    label = label.lower()
    if label[-1] == ':':
        label = label[:-1]
    
    column_title = ''
    if label in column_title_map.keys():
        column_title = column_title_map[label]
    
    return column_title

def getYomi(search_block, class_name='ony'):
    yomis = []
    yomi_elements = search_block.findAll('a', class_=class_name)
    if yomi_elements is not None and len(yomi_elements) > 0:
        for element in yomi_elements:
            yomis.append(element.getText())

    return yomis

def getExamples(search_block):
    examples = []
    ul_element = search_block.find('ul', class_='kanji-search-ul')
    if ul_element is None:
        return examples
    
    li_elements = ul_element.findAll('li')
    if li_elements is None or len(li_elements) == 0:
        return examples
    
    for element in li_elements:
        examples.append(element.getText())
    
    return examples

def getConstructs(search_block):
    constructs = []
    ul_element = search_block.find('ul', class_='kanji-search-ul')

    if ul_element is None:
        return constructs
    
    li_elements = ul_element.findAll('li')
    if len(li_elements) < 2 or li_elements is None:
        return constructs
    
    construct_elements = li_elements[1].findAll('span')
    if construct_elements is None or len(construct_elements) == 0:
        return constructs
    for element in construct_elements:
        text = element.getText()
        hanviet = element.get('title')
        constructs.append({
            'text': text,
            'hanviet': hanviet
        })
    
    return constructs


def getImage(search_block):
    image_url = ''
    image_element = search_block.find('img')
    if image_element is not None:
        image_url = image_element.get('src')
    
    return image_url

def getText(search_block):
    text = ''
    p_element = search_block.find('p')
    if p_element is not None:
        text = p_element.getText()

    return text

kanjis = []
for i in range(2, 4000):
    data['id'] = i

    response = requests.post(url, data= data, headers=headers)

    response_json = json.loads(response.text)

    response_content = response_json['Content']

    if response_content == '':
        continue

    kanji_obj = {
        'kanji_text': '',
        'hanviet': '',
        'onyomis': [],
        'kunyomis': [],
        'examples': [],
        'constructs': [],
        'image_url': '',
        'mean': '',
        'explain': '',
        'remember_trick': '',
        'level': '',
        'stroke_count': ''
    }

    soup = BeautifulSoup(response_content, 'html.parser')

    kanji_header = soup.find('div', class_='kanji-search-header')

    if kanji_header is None:
        continue

    kanji_text_element = kanji_header.find('span', class_='qqq')
    hanviet_element = kanji_header.find('span', class_='qqe')
    if kanji_text_element is None or hanviet_element is None:
        continue

    kanji_obj['kanji_text'] = kanji_text_element.getText()
    kanji_obj['hanviet'] = hanviet_element.getText()

    kanji_search_blocks = soup.findAll('div', class_='kanji-search-block')

    for block in kanji_search_blocks:
        label = block.find('label')
        if label is None:
            continue

        label_text = label.getText()
        if label_text is None or label_text == '':
            continue
        
        column_title = fromLabelToColumnTitle(label_text)

        if column_title == '':
            continue
        
        if column_title == 'onyomi':
            kanji_obj['onyomis'] = getYomi(block, class_name='ony')
        elif column_title == 'kunyomi':
            kanji_obj['kunyomis'] = getYomi(block, class_name='kuny')
        elif column_title == 'examples':
            kanji_obj['examples'] = getExamples(block)
        elif column_title == 'constructs':
            kanji_obj['constructs'] = getConstructs(block)
        elif column_title == 'memorable_img':
            kanji_obj['image_url'] = getImage(block)
        else: 
            kanji_obj[column_title] = getText(block)
        
    kanjis.append(kanji_obj)
    time.sleep(15)

with open('kanji.json', 'w', encoding='utf-8') as f:
    json.dump(kanjis, f, ensure_ascii=False)