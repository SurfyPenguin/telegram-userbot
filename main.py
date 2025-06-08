from pyrogram import Client
from config import API_ID, API_HASH

plugins = dict(root = "plugins")

with open("session.txt", "r") as file:
    session = file.read()

app = Client(
    name = "acc",
    session_string= session,
    plugins= plugins,
    in_memory = True,
)

if __name__ == "__main__":
    print("running...")
    app.run()
