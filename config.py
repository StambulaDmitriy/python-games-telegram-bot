from environs import Env


def config(key):
    env = Env()
    env.read_env('.env')

    variables = {
        'token': env.str("BOT_TOKEN"),
        'admins': list(map(int, env.list("ADMINS"))),
        'db_user': env.str("MONGODB_USERNAME"),
        'db_password': env.str("MONGODB_PASSWORD"),
        'db_address': env.str("MONGODB_ADDRESS"),
    }

    return variables[key]
