from environs import Env


def config(key):
    env = Env()
    env.read_env('.env')

    variables = {
        'token': env.str("BOT_TOKEN"),
        'admins': list(map(int, env.list("ADMINS")))
    }

    return variables[key]
