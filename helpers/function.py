import re
from datetime import datetime as d


def get_date_hour():
    return d.now().strftime("Le %d/%m/%Y à %H:%M:%S")


def get_list_attribut(my_obj):
    l_attribut = [
        attr for attr in my_obj.__dict__
        if not callable(getattr(my_obj, attr)) and not attr.startswith("_")
    ]
    return l_attribut


def validate_format(value, format):
    validate_format = re.match(format, value)
    if validate_format:
        return True
