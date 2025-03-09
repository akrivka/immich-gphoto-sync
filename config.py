import os
import dotenv
from pathlib import Path

# Try to load from data dir if specified in environment
data_folder = os.environ.get("DATA_FOLDER")
if data_folder:
    env_path = Path(data_folder) / ".env"
    if env_path.exists():
        dotenv.load_dotenv(dotenv_path=env_path)
else:
    # Fall back to current directory
    dotenv.load_dotenv()

IMMICH_URL = os.environ["IMMICH_URL"]
IMMICH_API_KEY = os.environ["IMMICH_API_KEY"]
DATA_FOLDER = Path(os.environ["DATA_FOLDER"] if "DATA_FOLDER" in os.environ else "./data")
ALBUMS_FILE = DATA_FOLDER / "albums.txt"
USER_DATA_FOLDER = DATA_FOLDER / "usrdata"
DB_FILE = DATA_FOLDER / "db.sqlite"
HEADLESS = bool(os.environ.get("HEADLESS", "true").lower() == "true")
