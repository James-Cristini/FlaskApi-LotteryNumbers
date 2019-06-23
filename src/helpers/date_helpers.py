from datetime import datetime
from errors import DataValidationError


DATE_FORMAT_1 = '%Y%M%d'
DATE_FORMAT_2 = '%M/%d/%Y'


def dto_to_str(dto):
    """ Convert datetime object to string of YYYYMMDD. """

    try:
        return datetime.strftime(dto, DATE_FORMAT_1)
    except ValueError:
        raise


def str_to_dto(sdt):
    """ There are two expected date formats for now.
        The former is preferred input and latter is format in the base datset. """

    try: # Try the first format, pass if fails
        return datetime.strptime(sdt, DATE_FORMAT_1)
    except ValueError as e:
        pass

    try: # Try the second format
        return datetime.strptime(sdt, DATE_FORMAT_2)
    except ValueError:
        raise


def validate_date(date):
    """ Ensures that date being used is ultimately in a consistent format, YYYYMMDD
        Raises DataValidationError if not of type """

    if isinstance(date, datetime):
        try:
            date = dto_to_str(date)
        except ValueError:
            pass # What to do in this case?
        else:
            return date

    if isinstance(date, str) or isinstance(date, unicode):
        try: # Convert to dto then back to string to ensure format is as expected
            date = str_to_dto(date)
            date = dto_to_str(date)
        except ValueError:
            pass
        else:
            return date

    raise DataValidationError("Date, {}, is not of an expected type (datetime object or string in format YYYYMMDD or MM/DD/YYYY".format(date))
