from django.core.exceptions import DisallowedHost
from django.http import UnreadablePostError
from pylibmc import Error as MemcachedError

EXCLUDED = (
    DisallowedHost,
    UnreadablePostError,
    MemcachedError,
)

def exclude_useless_errors(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        for excluded_class in EXCLUDED:
            if isinstance(exc_value, EXCLUDED):
                return False
    return True
