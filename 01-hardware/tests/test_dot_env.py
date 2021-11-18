# settings.py
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# settings.py
import os
SECRET_KEY = os.getenv("DEVADDR")
SECRET_KEY_mod= bytearray.fromhex(SECRET_KEY)
print(SECRET_KEY_mod)
print(type(SECRET_KEY_mod))

SECRET_KEY2 = bytearray([0x26, 0x01, 0x3D, 0x54])
print(SECRET_KEY2)
print(type(SECRET_KEY2))

print(SECRET_KEY2 == SECRET_KEY_mod)