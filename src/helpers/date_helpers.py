from datetime import datetime
from .errors import DataValidationError


def validate_date(dt):
    if isinstance(dt, datetime):
        return dt

    try:
        dt = datetime.strptime(dt, "%Y%M%d")
    except TypeError:
        # maybe handle ints?
        raise DataValidationError("Date: {0} is not a valid type, date, or format [expected format is YYYYMMDD]".format(dt))
    else:
        return dt
