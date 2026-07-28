from pathlib import Path
from enum import Enum, auto

APP_NAME = "WaveLength"
ORGANIZATION = "SML365"
VERSION = "v0.0.00"
FILEPATH = Path(__file__).parent
MAX_SIZE = 16777215

# --- Window Types --- #
class PanelType(Enum):
    SIDEBAR = auto()
    BROWSER = auto()
    TIMELINE = auto()
    MIXER = auto()
    BEAT_EDITOR = auto()
    SONG_EDITOR = auto()
    RESOURCE_MONITOR = auto()
    TEST_WINDOW = auto()