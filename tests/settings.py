import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
CRAFT_CFG = {
    "owner": os.environ.get("CRAFT_OWNER"),
    "token": os.environ.get("CRAFT_TOKEN"),
    "url": os.environ.get("CRAFT_URL") or "https://beta.craft.ai"
}
