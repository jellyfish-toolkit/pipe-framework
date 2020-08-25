from src.db.config import DB_STEP_CONFIG
from pipe.core.utils import configure
from pipe.generics.db.orator_orm.load import LDBInsertUpdateBase


@configure(DB_STEP_CONFIG)
class LDatabase(LDBInsertUpdateBase):
    pass
