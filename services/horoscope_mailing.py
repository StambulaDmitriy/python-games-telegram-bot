from handlers import horoscope_controller
from bootstrap import Database, MyBot
from handlers.horoscope_controller import zodiac_signs
from services import invert_dict


async def mail_all_subscribers():
    db = Database().getInstance()
    users_table = db.casino.users

    users_for_mailing = list(users_table.find({"is_subscribed_horoscope_mailing": True}))

    zodiak_signs = set([x["zodiak_sign"] for x in users_for_mailing])

    horoscops = {}
    for zodiak_sign in zodiak_signs:
        horoscops[zodiak_sign] = await horoscope_controller.get_horoscope(zodiak_sign, 'today')

    bot = MyBot().getInstance()

    for user in users_for_mailing:
        zodiak_sign = user['zodiak_sign']

        result_string = "Гороскоп <b>на сегодня</b> для знака зодиака: {}\n".format(invert_dict(zodiac_signs)[zodiak_sign])

        result_string += horoscops[zodiak_sign]

        await bot.send_message(user['_id'], result_string)
