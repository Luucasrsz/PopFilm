import html
import json
import bleach
import decimal

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def sanitize_input(user_input):

    escaped_input = html.escape(user_input)

    clean_input = bleach.clean(escaped_input)

    return clean_input