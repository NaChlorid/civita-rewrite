import shit_env

env = shit_env.Env(".env")

VERSION = env.Get("VERSION")
TOKEN = env.Get("TOKEN")
TOKEN_MISTRAL = env.Get("TOKEN_MISTRAL")

