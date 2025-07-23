import datetime

from flask_restx import abort

def date_check(start_date_str='', end_date_str=''):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    except ValueError:
        return abort(400, description="Dates must be in YYYY-MM-DD format.")
    finally:
        return start_date,end_date

