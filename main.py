from pyrogram import Client
from config import API_ID, API_HASH

plugins = dict(root = "plugins")

app = Client("my_account", plugins= plugins)


if __name__ == "__main__":
    print("running...")
    app.run()