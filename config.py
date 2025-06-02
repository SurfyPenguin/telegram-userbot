from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")

# config
CHUNK = 20
PREFIXES = ["?"]
AUTH_USERS = ["me"]

# DC info
DCS = {
    "DC1" : {"location" : "MIA, Miami FL, USA", "ip" : "149.154.175.53"},
    "DC2" : {"location" : "AMS, Amsterdam, NL", "ip" : "149.154.167.51"},
    "DC3" : {"location" : "MIA, Miami FL, USA", "ip" : "149.154.175.100"},
    "DC4" : {"location" : "AMS, Amsterdam, NL", "ip" : "149.154.167.91"},
    "DC5" : {"location" : "SIN, Singapore, SG", "ip" : "91.108.56.130"}
}
