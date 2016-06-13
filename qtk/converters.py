import QuantLib as ql
import datetime
from dateutil.parser import parse


class QuantLibFactory(object):

    _daycount_map = {
        "ACT/ACT": ql.ActualActual(),
        "ACTUAL/ACTUAL": ql.ActualActual(),
        "ACT/365": ql.ActualActual(),  # Per ISDA
        "ACTUAL/ACTUALBOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACT/ACTBOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACTUAL/ACTUALEURO": ql.ActualActual(ql.ActualActual.Euro),
        "ACT/ACTEURO": ql.ActualActual(ql.ActualActual.Euro),

        "ACTUAL/365BOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACT/365BOND": ql.ActualActual(ql.ActualActual.Bond),
        "ACTUAL/365EURO": ql.ActualActual(ql.ActualActual.Euro),
        "ACT/365EURO": ql.ActualActual(ql.ActualActual.Euro),

        "ACT/360": ql.Actual360(),
        "ACTUAL/360": ql.Actual360(),
        "A/360": ql.Actual360(),

        "30/360": ql.Thirty360(ql.Thirty360.USA),
        "360/360": ql.Thirty360(ql.Thirty360.USA),
        "BONDBASIS": ql.Thirty360(ql.Thirty360.USA),
        "30E/360": ql.Thirty360(ql.Thirty360.EurobondBasis),
        "EUROBONDBASIS": ql.Thirty360(ql.Thirty360.EurobondBasis),
        "30/360ITALIAN": ql.Thirty360(ql.Thirty360.Italian),

        "ACTUAL/365FIXED": ql.Actual365Fixed(),
        "ACT/365FIXED": ql.Actual365Fixed(),
        "A/365F": ql.Actual365Fixed(),

        "ACTUAL/365NOLEAP": ql.Actual365NoLeap(),
        "ACT/365NL": ql.Actual365NoLeap(),
        "NL/365": ql.Actual365NoLeap(),
        "ACTUAL/365JGB": ql.Actual365NoLeap(),
        "ACT/365JGB": ql.Actual365NoLeap(),
    }

    _freq_map = {
        "ANNUAL": ql.Annual,
        "SEMIANNUAL": ql.Semiannual,
        "QUARTERLY": ql.Quarterly,
        "BIMONTHLY": ql.Bimonthly,
        "MONTHLY": ql.Monthly,
        "BIWEEKLY": ql.Biweekly,
        "WEEKLY": ql.Weekly,
        "DAILY": ql.Daily
    }

    _day_convention_map = {
        "FOLLOWING": ql.Following,
        "F": ql.Following,
        "MODIFIEDFOLLOWING": ql.ModifiedFollowing,
        "MF": ql.ModifiedFollowing,
        "PRECEDING": ql.Preceding,
        "P": ql.Preceding,
        "MODIFIEDPRECEDING": ql.ModifiedPreceding,
        "MP": ql.ModifiedPreceding,
        "UNADJUSTED": ql.Unadjusted,
        "U": ql.Unadjusted,
        "HALFMONTHMODIFIEDFOLLOWING": ql.HalfMonthModifiedFollowing,
        "HMMF": ql.HalfMonthModifiedFollowing
    }

    @classmethod
    def to_daycount(cls, day_count):
        """
        Converts day count str to QuantLib object

        :param day_count: Day count
        :type day_count: str
        :return:
        """
        # remove spaces, parenthesis and capitalize
        day_count = day_count.upper().translate(None, " ()")
        return cls._daycount_map[day_count]

    @classmethod
    def to_frequency(cls, freq):
        freq = freq.upper().translate(None, " ")
        return  cls._freq_map[freq]

    @classmethod
    def to_date(cls, date):

        if isinstance(date, datetime.date ) or isinstance(date, datetime.datetime):
            ql_date = ql.Date(date.day, date.month, date.year)
        elif isinstance(date, str):
            d = parse(date)
            ql_date = ql.Date(d.day, d.month, d.year)
        elif isinstance(date, int):
            year, rest = divmod(date, 10000)
            month, day = divmod(rest, 100)
            ql_date = ql.Date(day, month, year)
        elif isinstance(date, ql.Date):
            ql_date = date
        else:
            raise ValueError("Unrecognized date format")
        return ql_date

    @classmethod
    def to_date_yyyymmdd(cls, date):
        if isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            yyyymmdd = date.year*10000 + date.month*100 + date.day
        elif isinstance(date, str):
            d = parse(date)
            yyyymmdd = d.year*10000 + d.month*100 + d.day
        elif isinstance(date, ql.Date):
            yyyymmdd = date.year()*10000 + date.month()*100 + date.dayOfMonth()
        elif isinstance(date, int):
            yyyymmdd = date
        else:
            raise ValueError("Unrecognized date format")
        return yyyymmdd

    @classmethod
    def to_date_py(cls, date):
        if isinstance(date, str):
            date_py = parse(date).date()
        elif isinstance(date, datetime.date) or isinstance(date, datetime.datetime):
            date_py = date
        elif isinstance(date, ql.Date):
            date_py = datetime.date(date.year(), date.month(),date.dayOfMonth())
        elif isinstance(date, int):
            year, rest = divmod(date, 10000)
            month, day = divmod(rest, 100)
            date_py = datetime.date(year, month, day)
        else:
            raise ValueError("Unrecognized date format")
        return date_py

    @classmethod
    def to_day_convention(cls, day_convention):
        day_convention = day_convention.upper().translate(None, " ")
        return cls._day_convention_map[day_convention]