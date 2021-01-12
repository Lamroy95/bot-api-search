header = "Плюсы <b>aiogram</b> и его преимущества перед telebot"
adv_list = [
    "Бот <b>не падает</b> на поллинге",
    "Наличие машины состояний (<a href='https://github.com/aiogram/aiogram/blob/dev-2.x/examples/finite_state_machine_example.py'>FSM</a>), а не тупого next_step_handler",
    "Наличие <a href='https://telegra.ph/Ispolzovanie-Middlwares-v-aiogram-08-14'>Middleware</a> и фильтров",
    "Поддержка API <b>день в день</b>: по статистике, аио выходит раньше других",
    "<b>Errors handler</b> и исключения (в телеботе общие исключения на все типы ошибок)",
    "В телеботе исходники без тайп хинтинга и автодополнение работает хуже",
    "Аиограм - это <b>полноценный фреймворк</b>, а не обёртка над апи (телебот - обёртка). Приятно смотреть на структуру",
    "Ведётся не только поддержка API, но и развитие самого фреймворка: в третьей версии будут улучшения в структуре и логике, новые фичи",
    "Адекватное комьюнити (не для нубов) (ru: @aiogram_ru, eng: @aiogram)",
]


async def get_advantages_article():
    result = f'{header}:'
    for i, item in enumerate(adv_list):
        result += f'\n{i+1}) {item}.'

    return result
