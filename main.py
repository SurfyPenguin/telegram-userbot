from pyrogram import Client
from config import API_ID, API_HASH

plugins = dict(root = "plugins")

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, plugins= plugins)


if __name__ == "__main__":
    print("running...")
    app.run()