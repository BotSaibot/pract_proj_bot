'''Парсер (веб-скрапер) объявлений с HeadHunter.'''
import logging
import aiohttp
import bs4


RESOURCE_URL = 'https://hh.ru/search/vacancy'
RESOURCE_HEADER = {'user-agent': 'py-parser/2.5'}


logger = logging.getLogger(__name__)


async def decoder_str_to_params(str_in: str, asserts_msgs, sep=' - ') -> dict:
    '''Decodes a string into parameters (dict).'''
    logger.info('decoder_str_to_params() is running...')
    out = {}
    for snum, sline in enumerate(str_in.splitlines()):
        assert_message = asserts_msgs['no separator'].format(
            snum, sline, sep)
        assert sep in sline, assert_message
        key, val = sline.split(sep=sep)
        if val.isdigit():
            val = int(val)
        elif ', ' in val:
            val = val.split(sep=', ')
        out[key] = val

    return out


async def decoder_str_to_page(str_in: str, asserts_msgs, max_int: int) -> int:
    '''Decodes a string into page (int).'''
    assert str_in.isdigit(), asserts_msgs['not a digit']
    out = int(str_in)
    assert 0 < out <= max_int, asserts_msgs['invalid digit'].format(max_int)
    return out - 1


async def get_general_info(doc: bs4.BeautifulSoup, params: dict) -> tuple:
    '''Gets the host URL, total number of results,
    and total number of pages.'''
    logger.info('get_general_info() is running...')

    host_url = doc.find('link', {'rel': 'canonical'})['href']
    host_url = host_url.replace('/search/vacancy', '')

    total_results = min(int(
        ''.join(bs4.re.findall(
            r'\d+',
            doc.find('h1', {'class': 'bloko-header-section-3'}).getText())
        )), 2000)
    if params.get('items_on_page') is not None:
        total_pages = (total_results // params['items_on_page']
                       + (total_results % params['items_on_page'] > 0))
    else:
        total_pages = 0

    return host_url, total_results, total_pages


async def get_response(**kwargs) -> bs4.BeautifulSoup:
    '''Возвращает проанализированный HTML-документ ответа от ресурса по URL
    адресу.'''
    logger.info('get_response() is running...')
    assert 'url' in kwargs, '''The 'url' keyword argument was not passed!'''
    timeout = aiohttp.ClientTimeout(total=6)
    logger.debug(
        'create session %r with parameters %r',
        kwargs['url'], kwargs.get('params')
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs, timeout=timeout) as response:

            response.raise_for_status()
            # FIXME: catching the exception # [fixme]
            # aiohttp.client_exceptions.ClientResponseError: 502,
            # message='Bad Gateway', url=URL('https://google.com')
            check = 'text/html' in response.headers.get('Content-Type')
            logger.debug(
                'session response status %s, content-type %r',
                response.status, response.headers.get('Content-Type')
            )
            html = await response.text()

    assert check, 'Response has the wrong content-type!'
    soup = bs4.BeautifulSoup(html, 'html.parser', multi_valued_attributes=None)
    return soup


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
