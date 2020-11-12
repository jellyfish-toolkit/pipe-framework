import valideer

from pipe.core.decorators import configure
from pipe.server import PipeRequest
from src.db.config import DB_STEP_CONFIG
from pipe.generics.db.orator_orm.extract import EDBReadBase


@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    required_fields = {
        '+request': valideer.Type(PipeRequest)
    }
