from decimal import Decimal
from json import JSONEncoder


class TestJSONEncoder(JSONEncoder):
    """
    Serialize Decimal instances as strings
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return JSONEncoder.default(self, obj)
