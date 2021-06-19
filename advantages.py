header = "Плюсы <b>aiogram</b>"
adv_list = [
    "Бот <b>не падает</b> на поллинге",
    "Полноценная асинхронность, а не <a href='https://github.com/eternnoir/pyTelegramBotAPI/blob/07d198aebe626716bbd69bab8f9031d873fcc98b/telebot/util.py#L142'>треды</a>",
    "<a href='https://github.com/aiogram/aiogram/blob/dev-2.x/examples/finite_state_machine_example.py'>FSM</a> вместо next_step_handler",
    "<a href='https://github.com/aiogram/aiogram/tree/dev-2.x/aiogram/dispatcher/filters'>Фильтры</a> и нормальные <a href='https://telegra.ph/Ispolzovanie-Middlwares-v-aiogram-08-14'>Middleware</a>",
    "<a href='https://t.me/aiogram_ru/648815'>Magic-фильтры</a>",
    "Оперативные обновления",
    "<b>Errors handler</b> и <a href='https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/utils/exceptions.py'>исключения</a> для большинства типов ошибок",
    "Все функции аннотированы и документированны",
    "Аиограм - это <b>фреймворк</b>, а не обёртка над апи",
    "Развитие фреймворка: скоро 🌚 будет релиз <a href='https://github.com/aiogram/aiogram/tree/dev-3.x'>третьей версии</a>",
    "Большое комьюнити: @aiogram_ru",
]


async def get_advantages_article():
    result = f'{header}:'
    for i, item in enumerate(adv_list):
        result += f'\n{i+1}) {item}.'

    return result
