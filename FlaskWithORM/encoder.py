from flask.json import JSONEncoder

from FlaskWithORM.models.models import User


class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "name": obj.name,
                "email": obj.email
            }
        return super(Encoder, self).default(obj)