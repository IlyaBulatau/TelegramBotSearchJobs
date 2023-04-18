from environs import Env

def load_token():
    """
    Загружает токен из окружения
    """
    env = Env()
    env.read_env()
    token= env('TOKEN')
    return token
