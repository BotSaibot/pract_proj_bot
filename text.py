'''Texts for bot'''
# buttons
BUTTON_BACK_TO_MAIN_MENU = '↩ Выйти в меню'
BUTTON_DEBUG = '⚙ Отладка'
BUTTON_HELP = '🔎 Помощь'
BUTTON_SHOW_ID = '🆔 Мой идентификатор'
BUTTON_PARSER = '🪄 Парсер'
BUTTON_NAV_PARSER_PRE = '◀️ Пред'
BUTTON_NAV_PARSER_NEXT = ' ▶️ След'
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
TEXT_PARSER_PARAMS_EXAMPLE1 = (
    'Пример:\n\nenable_snippets - False\nitems_on_page - 2\nonly_with_salary -'
    ' True\norder_by - publication_time\nored_clusters - True\npart_time - tem'
    'porary_job_true\nprofessional_role - 96\nsalary - 270000\nsearch_field - '
    'name, company_name, description\nstatus - non_archived\ntext - python'
)
TEXT_SHOW_ID = '{name}, Ваш ID: {id}.'
