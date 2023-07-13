'''Парсер (веб-скрапер) объявлений с HeadHunter.'''
import aiohttp
import bs4
import logging
import requests


RESOURCE_URL = 'https://hh.ru/search/vacancy'
RESOURCE_HEADER = {'user-agent': 'py-parser/2.3'}


logger = logging.getLogger(__name__)


async def get_response(**kwargs) -> bs4.BeautifulSoup:
    '''Возвращает проанализированный HTML-документ ответа от ресурса по URL
    адресу.'''
    logger.info('get_response() is running...')
    assert 'url' in kwargs
    # response = requests.get(**kwargs, timeout=4)
    timeout = aiohttp.ClientTimeout(total=6)
    logger.debug(
        f'create session {kwargs["url"]!r} with parameters '
        f'{kwargs.get("params")!r}'
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs, timeout=timeout) as response:

            response.raise_for_status()
            check = 'text/html' in response.headers.get('Content-Type')
            logger.debug(
                'session response status %s, content-type %r',
                response.status, response.headers.get('Content-Type')
            )
            html = await response.text()

    assert check, 'Response has the wrong content-type!'
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def tree_traversal(doc: bs4.BeautifulSoup, params: dict) -> dict:
    '''Рекурсивный обход дерева полного графа, возвращает словарь.
    Т.е. здесь извлекаем из HTML-документа только полезную информацию.'''
    logger.info('tree_traversal() is running...')
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


async def get_general_info(doc: bs4.BeautifulSoup, params: dict) -> tuple:
    '''Gets the host URL, total number of results,
    and total number of pages.'''
    logger.info('get_general_info() is running...')

    host_url = doc.find('link', {'rel': 'canonical'})['href']
    host_url = host_url.replace('/search/vacancy', '')
    # 'https://voronezh.hh.ru/search/vacancy'

    total_results = int(
        # doc.find('h1',
        #          {'class': 'bloko-header-section-3'}).getText().split()[0]
        ''.join(
            bs4.re.findall(
                r'\d+',
                doc.find('h1', {'class': 'bloko-header-section-3'}).getText())
        )
    )
    if params.get('items_on_page') is not None:
        total_pages = (total_results // params['items_on_page']
                       + (total_results % params['items_on_page'] > 0))
    else:
        total_pages = 0

    return host_url, total_results, total_pages


async def simply_traversal(doc: bs4.BeautifulSoup, host: str, index=0) -> dict:
    '''Простой обход документа'''
    logger.info('simply_traversal() is running...')

    out = {}

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

        url = f'{host}/vacancy/{key}'

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
    logger.info('data_to_file() is running...')
    with open(f_name, 'w', encoding='utf-8') as fout:

        for index, value in data.items():
            key, name, area, salary, url, employer = value.values()

            out = (f'''{index} {key} {url}\n\t{name}\n\t'''
                   f''''{employer}', {area}\n\t{salary}\n\n''')

            fout.write(out)
    logger.debug('data_to_file() -> the %r file has been written', f_name)


async def decoder_str_to_params(str_in: str, sep=' - ') -> dict:
    '''Decodes a string into parameters (dict).'''
    logger.info('decoder_str_to_params() is running...')
    out = {}
    for snum, sline in enumerate(str_in.splitlines()):
        assert_message = (
            f'Line {snum} {sline!r} does not have a {sep!r} separator!'
        )
        assert sep in sline, assert_message
        key, val = sline.split(sep=sep)
        if val.isdigit():
            val = int(val)
        elif ', ' in val:
            val = val.split(sep=', ')
        out[key] = val

    return out


def main() -> None:
    '''Главная функция.'''
    logger.info('main() is running...')

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
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='[%(asctime)s:%(msecs)03d] %(levelname)s:%(name)s:%(message)s',
    #     datefmt='%d.%m.%Y %H:%M:%S'
    # )
    logger.info('Start bs4_based_parser.py')
    main()
