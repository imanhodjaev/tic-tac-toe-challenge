import sys
from enum import Enum
import databases
import orm
import sqlalchemy


BD_URI = "sqlite:///db.sqlite"
if "pytest" in sys.argv[0]:
    BD_URI = "sqlite:///test-db.sqlite"

database = databases.Database(BD_URI)
metadata = sqlalchemy.MetaData()


class GameStatus(Enum):
    pending: str = "pending"
    done: str = "done"
    cancelled: str = "cancelled"


class Game(orm.Model):
    __tablename__ = "notes"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    state = orm.String(max_length=18)
    owner = orm.JSON()
    challenger = orm.JSON(default={}, allow_null=True)
    winner = orm.Integer(allow_null=True)
    status = orm.String(max_length=10)


# Create the database
engine = sqlalchemy.create_engine(str(database.url), connect_args={"check_same_thread": False})
metadata.create_all(engine)
