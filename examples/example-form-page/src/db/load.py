from pipe.core.decorators import configure
from src.db.config import DB_STEP_CONFIG
from pipe.generics.db.orator_orm.load import LDBInsertUpdateBase, LDatabaseDeleteBase


@configure(DB_STEP_CONFIG)
class LDatabase(LDBInsertUpdateBase):
    pass

@configure(DB_STEP_CONFIG)
class LDelete(LDatabaseDeleteBase):
    pass
