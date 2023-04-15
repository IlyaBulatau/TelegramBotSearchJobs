from environs import Env

def load_token():
    env = Env()
    env.read_env()
    token= env('TOKEN')
    return token
