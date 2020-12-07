import valideer

from pipe.server.http.extract import EJsonBody


class ETodoJsonBody(EJsonBody):
    required_fields = {
        **EJsonBody.required_fields,
        **{
            '+id': valideer.Type(int, str)
        }
    }
