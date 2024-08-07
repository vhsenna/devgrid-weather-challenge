from sqlalchemy.ext.declarative import DeclarativeMeta

from src.db.base import Base


def test_base_creation():
    assert isinstance(
        Base, DeclarativeMeta), "Base should be an instance of DeclarativeMeta"
