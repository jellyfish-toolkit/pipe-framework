import valideer

from pipe.core.decorators import validate, configure
from pipe.server import PipeRequest
from src.db.config import DB_STEP_CONFIG
from pipe.generics.db.orator_orm.extract import EDBReadBase


@validate({
    '+request': valideer.Type(PipeRequest)
})
@configure(DB_STEP_CONFIG)
class EDatabase(EDBReadBase):
    pass


@validate({
    '+{pk_field}': valideer.Type(int)
})
class ETodoById(EDatabase):
    pass
