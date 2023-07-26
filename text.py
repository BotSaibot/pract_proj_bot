'''Texts for bot'''
buttons = {
    'back to': {
        'main menu': '↩ Выйти в меню',
        'parser': '↩ Назад'
    },
    'debug': '⚙ Отладка',
    'help': '🔎 Помощь',
    'parser': {
        'main': '🪄 Парсер',
        'nav': {
            'go to': {
                'end': '⏭',
                'page': '{page}/{pages}',
                'start': '⏮',
            },
            'next': '⏩',
            'pre': '⏪'
        },
        'params': '⚙ Изменить параметры',
        'start': '🚀 Запуск'
    },
    'show id': '🆔 Мой идентификатор'
}
# layouts
layouts = {
    'cancel_handler': {
        'text': (
            'Команда {} отменена.\nОтправьте /help для получения списка команд'
            '.'
        )
    },
    'debug_message_handler': {
        'text': '⚙ Это отладочное сообщение! ⚙'
    },
    'help_handler': {
        'text': (
            '<b>Команды:</b>\n\t\t\t\t/start — показать приветственное сообщен'
            'ие и отобразить меню;\n\t\t\t\t/show_id — показать ваш идентифика'
            'тор;\n\t\t\t\t/main_menu — вызвать главное меню;\n\t\t\t\t/help —'
            ' показать эту справочную информацию;\n\t\t\t\t/cancel - отменена '
            'текущей операции\n\t\t\t\t/debug — показать отладочное сообщение.'
        )
    },
    'main_menu_handler': {
        'text': '☰ Главное меню'
    },
    'message_handler': {
        'edit_params': {
            'text': '<b>Успех!</b> Параметры парсера обновлены.',
            'no separator': 'Строка {} {!r} не имеет разделителя {!r}!'
        },
        'go_to_page': {
            'not a digit': 'Это не цифры.',
            'invalid digit': 'Это цифры, но не в диапазоне (0, {}].'
        },
        'try': '<b>Попробуйте ещё раз.</b>',
    },
    'parser_go_to_page_handler': {
        'text': (
            'Пришлите мне номер страницы. (0 &lt; Номер &lt;= {amt})\n<b>Испол'
            'ьзуйте только цифры.</b>'
        )
    },
    'parser_handler': {
        'bottom': '{0}\n{1} -> Finded {2}, results per page {3}',
        'text': '[{0}] {1} {5}\n\t{2}\n\t{6!r}, {3}\n\t{4}\n'
    },
    'parser_nav_transition_failure': {
        'next_end': '⚠ Вы уже на последней странице ⚠',
        'other': '⚠ Отказ в переключении ⚠',
        'pre_start': '⚠ Вы уже на первой странице ⚠'
    },
    'parser_set_params': {
        'example1': (
            'Пример 1:\n\nenable_snippets - False\nitems_on_page - 2\nonly_wit'
            'h_salary - True\norder_by - publication_time\nored_clusters - Tru'
            'e\npart_time - temporary_job_true\nprofessional_role - 96\nsalary'
            ' - 270000\nsearch_field - name, company_name, description\nstatus'
            ' - non_archived\ntext - python'
        ),
        'example2': (
            'Пример 2:\n\nenable_snippets - False\nexperience - noExperience\n'
            'items_on_page - 2\norder_by - publication_time\nored_clusters - T'
            'rue\nprofessional_role - 96\nschedule - remote\nsearch_field - na'
            'me, company_name, description\nstatus - non_archived\ntext - pyth'
            'on'
        ),
        'text': (
            'ХОРОШО. Пришлите мне список параметров. Пожалуйста, используйте э'
            'тот формат:\n\nпараметр1 - значение\nпараметр2 - другое значение'
        )
    },
    'show_id_handler': {
        'text': '{name}, Ваш ID: {id}. Статус: {status!r}'
    },
    'start_handler': {
        'text': 'Привет, {name}, я бот ☺️'
    }
}
