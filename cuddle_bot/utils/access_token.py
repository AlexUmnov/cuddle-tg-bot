import os

def get_access_token() -> str:
    try:
        return os.environ['ACCESS_TOKEN']
    except KeyError as e:
        raise RuntimeError("You need to set up ACCESS_TOKEN env var")