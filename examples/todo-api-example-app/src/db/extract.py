import valideer

from pipe.core import PipeRequest
from src.db.config import DB_STEP_CONFIG
from pipe.core.utils import configure, validate
from pipe.generics.db.orator_orm.extract import EDBReadBase


@validate({
    '+request': valideer.Type(PipeRequest)
})
@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass
