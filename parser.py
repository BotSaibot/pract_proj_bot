'''Парсер (веб-скрапер) объявлений с HeadHunter.'''
import bs4
import logging
import requests


RESOURCE_URL = 'https://hh.ru/search/vacancy'
RESOURCE_HEADER = {'user-agent': 'py-parser/2.3'}


def get_response(**kwargs) -> bs4.BeautifulSoup:
    '''Возвращает проанализированный HTML-документ ответа от ресурса по URL
    адресу.'''
    response = requests.get(**kwargs, timeout=4)
    response.raise_for_status()
    logging.info(f'''get_response({kwargs['url']!r}) {response.url!r}''')
    check = 'text/html' in response.headers.get('Content-Type')
    assert check, 'Response has the wrong content-type!'
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup


def tree_traversal(doc: bs4.BeautifulSoup, params: dict) -> dict:
    '''Рекурсивный обход дерева полного графа, возвращает словарь.
    Т.е. здесь извлекаем из HTML-документа только полезную информацию.'''
    logging.info(f'''tree_traversal''')
    out = {}
    index = 0

    host_url = requests.urllib3.get_host(
        doc.find('link', {'rel': 'canonical'})['href']
    )

    total_pages = int(
        doc.find('h1',
                 {'class': 'bloko-header-section-3'}).getText().split()[0]
    )
    total_pages = (total_pages // params['items_on_page']
                   + (total_pages % params['items_on_page'] > 0))

    for page_num in range(total_pages):

        if page_num != 0:
            params.update([('page', page_num),
                           ('hhtmFrom', 'vacancy_search_list')])
            doc = get_response(
                url=RESOURCE_URL,
                headers=RESOURCE_HEADER,
                params=params
            )

        for item in doc.find_all('div', {'class': 'serp-item'}):

            index += 1
            vacancy_response = item.find(
                'a', {'data-qa': 'vacancy-serp__vacancy_response'}
                )

            name = item.find('a', {'class': 'serp-item__title'})
            key = bs4.re.search(r'[0-9]+', name['href'])[0]
            name = name.getText() + (' [ARCHIVED]'
                                     if vacancy_response is None else '')

            area = item.find(
                'div', {'data-qa': 'vacancy-serp__vacancy-address'}
                ).getText()

            salary = item.find(
                'span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary is not None:
                salary = salary.getText().replace('\u202f', '')

            url = host_url[0] + '://' + host_url[1] + '/vacancy/' + key
            employer = item.find(
                'a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            if employer is not None:
                employer = employer.getText().replace('\xa0', ' ')
            else:
                employer = item.find(
                    'div', {'class': 'vacancy-serp-item__meta-info-company'}
                    ).getText().replace('\xa0', ' ')

            out[index] = {'key': key, 'name': name, 'area': area,
                          'salary': salary, 'url': url, 'employer': employer}

    return out


def data_to_file(data: dict, f_name: str) -> None:
    '''Записывает словарь в файл в кодировке UTF-8.'''
    logging.info(f'''data_to_file({f_name!r})''')
    with open(f_name, 'w', encoding='utf-8') as fout:

        for index, value in data.items():
            key, name, area, salary, url, employer = value.values()

            out = (f'''{index} {key} {url}\n\t{name}\n\t'''
                   f''''{employer}', {area}\n\t{salary}\n\n''')

            fout.write(out)


def main() -> None:
    '''Главная функция.'''
    logging.debug('main()')
    params = {
        'text': 'python',
        'part_time': 'temporary_job_true',
        'professional_role': 96,
        'search_field': ['name', 'company_name', 'description'],
        'enable_snippets': False,
        'salary': 270_000,
        'items_on_page': 20,
        'only_with_salary': True,
        'ored_clusters': True,
        'order_by': 'publication_time',
        'status': 'non_archived'
    }

    response = get_response(
        url=RESOURCE_URL,
        headers=RESOURCE_HEADER,
        params=params
        )

    response = tree_traversal(response, params)
    data_to_file(response, './output.txt')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s:%(msecs)03d] %(levelname)s:%(name)s:%(message)s',
        datefmt='%d.%m.%Y %H:%M:%S'
    )
    logging.info('Start parser.py')
    main()
