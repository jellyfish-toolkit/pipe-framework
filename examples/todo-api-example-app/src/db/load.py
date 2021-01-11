from pipe.core.decorators import configure
from pipe.generics.db.orator_orm.load import LDatabaseDeleteBase, LDBInsertUpdateBase

from src.db.config import DB_STEP_CONFIG


@configure(DB_STEP_CONFIG)
class LDatabase(LDBInsertUpdateBase):
    pass


@configure(DB_STEP_CONFIG)
class LDelete(LDatabaseDeleteBase):
    pass
