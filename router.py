from aiogram import F
from aiogram.filters import Command

import keyboards
from bootstrap import MyDispatcher

import handlers
from handlers import dice_game_controller, roulette_game_controller, bagels_game_controller
from keyboards.inline import HelpCallbackData
from states.bagels_game_states import BagelsGameStates
from states.dice_game_states import DiceGameStates
from states.roulette_game_states import RouletteGameStates


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
