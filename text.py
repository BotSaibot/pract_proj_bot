'''Texts for bot'''
# buttons
BUTTON_BACK_TO_MAIN_MENU = '↩ Выйти в меню'
BUTTON_BACK_TO_PARSER = '↩ Назад'
BUTTON_DEBUG = '⚙ Отладка'
BUTTON_HELP = '🔎 Помощь'
BUTTON_NAV_PARSER_NEXT = ' ▶️ След'
BUTTON_NAV_PARSER_PRE = '◀️ Пред'
BUTTON_PARSER = '🪄 Парсер'
BUTTON_PARSER_PARAMS = '⚙ Изменить параметры'
BUTTON_PARSER_START = '🚀 Запуск'
BUTTON_SHOW_ID = '🆔 Мой идентификатор'
# layouts
TEXT_GREET = 'Привет, {name}, я бот ☺️'
TEXT_HELP = ('<b>Команды:</b>\n'
             '\t\t\t\t/start — показать приветственное сообщение и отобразить '
             'меню;\n'
             '\t\t\t\t/show_id — показать ваш идентификатор;\n'
             '\t\t\t\t/main_menu — вызвать главное меню;\n'
             '\t\t\t\t/help — показать эту справочную информацию;\n'
             '\t\t\t\t/debug — показать отладочное сообщение.')
TEXT_MAIN_MENU_TITLE = '☰ Главное меню'
TEXT_PARSER_PARAMS = ('ХОРОШО. Пришлите мне список параметров. Пожалуйста, '
                      'используйте этот формат:\n\nпараметр1 - значение\n'
                      'параметр2 - другое значение')
TEXT_PARSER_PARAMS_SUCCESS = 'Успех! Параметры парсера обновлены.'
TEXT_PARSER_PARAMS_EXAMPLE1 = (
    'Пример 1:\n\nenable_snippets - False\nitems_on_page - 2\nonly_with_salary'
    ' - True\norder_by - publication_time\nored_clusters - True\npart_time - t'
    'emporary_job_true\nprofessional_role - 96\nsalary - 270000\nsearch_field '
    '- name, company_name, description\nstatus - non_archived\ntext - python'
)
TEXT_PARSER_PARAMS_EXAMPLE2 = (
    'Пример 2:\n\nenable_snippets - False\nexperience - noExperience\nitems_on'
    '_page - 2\norder_by - publication_time\nored_clusters - True\nprofessiona'
    'l_role - 96\nschedule - remote\nsearch_field - name, company_name, descri'
    'ption\nstatus - non_archived\ntext - python'
)
TEXT_SHOW_ID = '{name}, Ваш ID: {id}.'
