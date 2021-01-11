from pipe.core.decorators import configure
from pipe.generics.db.orator_orm.extract import EDBReadBase

from src.db.config import DB_STEP_CONFIG


@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass
