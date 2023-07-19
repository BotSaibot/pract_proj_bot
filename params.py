'''Params'''
# import asyncpg
import logging
import json


logger = logging.getLogger(__name__)

test = {
    'someid666': {
        'status': None,
        'parser_params': {
            'text': 'python',
            'part_time': 'temporary_job_true',
            'professional_role': 96,
            'search_field': ['name', 'company_name', 'description'],
            'enable_snippets': False,
            'salary': 270000,
            'items_on_page': 10,
            'only_with_salary': True,
            'ored_clusters': True,
            'order_by': 'publication_time',
            'status': 'non_archived'
        }
    }
}


def unload_params(params):
    '''Unloads params to the file'''
    logger.info('unload_params() is running...')
    with open('./data.json', 'w', encoding='UTF-8') as fout:
        fout.write(json.dumps(params, indent=4))


def load_params():
    '''Loads params from the file'''
    logger.info('load_params() is running...')
    with open('./data.json', 'r', encoding='UTF-8') as fin:
        return json.loads(fin.read())


def main():
    '''Main function'''
    msg = 'Are you sure you want to clear the parameter data? (Yes/No)\n'
    answer = input(msg)
    while answer.lower() not in ('n', 'nay', 'nix', 'no',
                                 'nope', 'not', 'cancel'):
        if answer.lower() in ('y', 'yes', 'yeah', 'yep', 'yes', 'yup'):
            unload_params({})
            print('Operation done')
            break
        print('Incorrect answer, please try again or cancel. (Cancel)\n')
        answer = input(msg)
    else:
        print('Operation canceled')


if __name__ == '__main__':
    main()
