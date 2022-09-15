def validate_bet(bet, user_balance):
    if not bet.isdigit():
        return "Вы ввели невалидное число. Используйте только цифры."

    if int(bet) > user_balance:
        return f"На вашем балансе недостаточно средств. Доступный депозит: ${user_balance}"

    if int(bet) < 10:
        return "Минимальная ставка $10"

    return True
