from aiogram import F
from aiogram.filters import Command

import keyboards
from bootstrap import MyDispatcher

import handlers
from filters import IsAdmin
from handlers import dice_game_controller, roulette_game_controller, bagels_game_controller, blackjack_game_controller, \
    support_chat_controller, horoscope_controller, magic_8_ball_controller
from keyboards.inline import HelpCallbackData
from states import AdminSupportStates, BagelsGameStates, BlackjackGameStates, DiceGameStates, HoroscopeStates, \
    RouletteGameStates, UserSupportStates, Magic8BallStates


def register_commands():
    dp = MyDispatcher().getInstance()

    dp.message.register(handlers.start, Command(commands='start'), state=None)

    dp.message.register(handlers.help_command, Command(commands='help'))
    dp.message.register(handlers.help_command, F.text == keyboards.main_menu_keyboard.RULES_BUTTON_TEXT, state=None)
    dp.callback_query.register(handlers.help_inline_callback, HelpCallbackData.filter())

    dp.message.register(handlers.balance_command, F.text == keyboards.main_menu_keyboard.BALANCE_BUTTON_TEXT, state=None)
    dp.message.register(handlers.balance_command, Command(commands='balance'), state=None)

    dp.message.register(handlers.halyava_command, F.text == keyboards.main_menu_keyboard.HALYAVA_BUTTON_TEXT, state=None)
    dp.message.register(handlers.halyava_command, Command(commands='halyava'))

    dp.message.register(dice_game_controller.start, F.text == keyboards.main_menu_keyboard.DICE_BUTTON_TEXT, state=None)
    dp.message.register(dice_game_controller.start, Command(commands='dice'), state=None)
    dp.message.register(dice_game_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, DiceGameStates.BetPending)
    dp.message.register(dice_game_controller.handle_bet, DiceGameStates.BetPending)

    dp.message.register(roulette_game_controller.start, F.text == keyboards.main_menu_keyboard.ROULETTE_BUTTON_TEXT, state=None)
    dp.message.register(roulette_game_controller.start, Command(commands='roulette'), state=None)
    dp.message.register(roulette_game_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, RouletteGameStates.BetSumPending)
    dp.message.register(roulette_game_controller.handle_bet_sum, RouletteGameStates.BetSumPending)
    dp.message.register(roulette_game_controller.return_to_bet, F.text == keyboards.roulette_bet_places_keyboard.BACK_TO_CHOOSE_BET_SUM, RouletteGameStates.BetPlacePending)
    dp.message.register(roulette_game_controller.handle_bet_place, RouletteGameStates.BetPlacePending)

    dp.message.register(bagels_game_controller.start, F.text == keyboards.main_menu_keyboard.BAGELS_BUTTON_TEXT, state=None)
    dp.message.register(bagels_game_controller.start, Command(commands='bagels'), state=None)
    dp.message.register(bagels_game_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, BagelsGameStates.BetPending)
    dp.message.register(bagels_game_controller.handle_bet, BagelsGameStates.BetPending)
    dp.message.register(bagels_game_controller.check_answer, BagelsGameStates.NumberGuessing)

    dp.message.register(blackjack_game_controller.start, F.text == keyboards.main_menu_keyboard.BLACKJACK_BUTTON_TEXT, state=None)
    dp.message.register(blackjack_game_controller.start, Command(commands='blackjack'), state=None)
    dp.message.register(blackjack_game_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, BlackjackGameStates.BetPending)
    dp.message.register(blackjack_game_controller.handle_bet, BlackjackGameStates.BetPending)
    dp.message.register(blackjack_game_controller.handle_user_choice, BlackjackGameStates.UserPlaying)

    dp.message.register(support_chat_controller.user_initiates, F.text == keyboards.main_menu_keyboard.SUPPORT_BUTTON_TEXT, state=None)
    dp.message.register(support_chat_controller.user_initiates, Command(commands='support'), state=None)
    dp.message.register(support_chat_controller.user_cancel_chat, Command(commands='cancel'), UserSupportStates.ConnectionPending)
    dp.message.register(support_chat_controller.user_pending_connection, UserSupportStates.ConnectionPending)
    dp.message.register(support_chat_controller.user_cancel_chat, Command(commands='cancel'), UserSupportStates.Talking)
    dp.message.register(support_chat_controller.user_talking, UserSupportStates.Talking)
    dp.callback_query.register(support_chat_controller.admin_accept_inline, F.data == 'support:next')
    dp.message.register(support_chat_controller.admin_accept, Command(commands='next'), IsAdmin(), state=None)
    dp.message.register(support_chat_controller.admin_cancel_chat, Command(commands='cancel'), AdminSupportStates.Talking)
    dp.message.register(support_chat_controller.admin_talking, AdminSupportStates.Talking)

    dp.message.register(horoscope_controller.horoscope_command, F.text == keyboards.main_menu_keyboard.HOROSCOPE_BUTTON_TEXT, state=None)
    dp.message.register(horoscope_controller.horoscope_command, Command(commands='horoscope'), state=None)
    dp.message.register(horoscope_controller.handle_zodiak_sign, HoroscopeStates.SelectingSign)
    dp.message.register(horoscope_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, HoroscopeStates.SelectingPeriod)
    dp.message.register(horoscope_controller.handle_horoscope_period, HoroscopeStates.SelectingPeriod)

    dp.message.register(magic_8_ball_controller.start, F.text == keyboards.main_menu_keyboard.MAGIC_8_BALL_BUTTON_TEXT, state=None)
    dp.message.register(magic_8_ball_controller.return_to_menu, F.text == keyboards.back_to_menu_keyboard.BACK_TO_MENU_BUTTON_TEXT, Magic8BallStates.QuestionPending)
    dp.message.register(magic_8_ball_controller.answer, Magic8BallStates.QuestionPending)
