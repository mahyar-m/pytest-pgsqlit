import sys
from unittest.mock import MagicMock

sys.modules['psycopg2'] = MagicMock()
sys.modules['psycopg2.extensions'] = MagicMock()
sys.modules['psycopg2._psycopg'] = MagicMock()

pytest_plugins = [
    "src.pytest_pgsqlit.plugin",
    "pytester"
]
