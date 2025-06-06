from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")

# config
CHUNK = 20
PREFIXES = ["?"]
AUTH_USERS = ["me"]

# Music/Video stream config
TITLE_LIMIT = 40
MUSIC_PREFIXES = ["!"]

# DC info
DCS = {
    1 : {"location" : "MIA, Miami FL, USA", "ip" : "149.154.175.53"},
    2 : {"location" : "AMS, Amsterdam, NL", "ip" : "149.154.167.51"},
    3 : {"location" : "MIA, Miami FL, USA", "ip" : "149.154.175.100"},
    4 : {"location" : "AMS, Amsterdam, NL", "ip" : "149.154.167.91"},
    5 : {"location" : "SIN, Singapore, SG", "ip" : "91.108.56.130"}
}
