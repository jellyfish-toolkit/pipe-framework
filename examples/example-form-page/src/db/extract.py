from pipe.core.decorators import configure
from src.db.config import DB_STEP_CONFIG
from pipe.generics.db.orator_orm.extract import EDBReadBase


@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass
