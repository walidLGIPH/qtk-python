from qtk.fields import Field as F
import QuantLib as ql
from qtk.common import Category as C
from qtk.templates import Instrument
from .common import CreatorBase
from qtk.templates import Template as T
from . import _creatorslog
from .utils import ScheduleCreator

# Fill the req and opt fields properly

class FixedRateBondCreator(CreatorBase):
    _templates = [T.INST_BOND_TBOND, T.INST_BOND_TBOND_HELPER]
    _req_fields = [F.SETTLEMENT_DAYS]
    _opt_fields = []

    def _create(self, asof_date):
        schedule = ScheduleCreator(self.data).create(asof_date)
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        face_amount = self.get(F.FACE_AMOUNT, 100.0)
        coupon = self.get(F.COUPON, 0.0)
        issue_date = self.get(F.ISSUE_DATE) or self.get(F.ASOF_DATE) or asof_date
        pay_calendar = self.get(F.PAYMENT_CALENDAR) or self.get(F.ACCRUAL_CALENDAR)
        pay_basis = self.get(F.PAYMENT_BASIS) or self.get(F.ACCRUAL_BASIS)
        pay_convention = self.get(F.PAYMENT_DAY_CONVENTION) or self.get(F.ACCRUAL_DAY_CONVENTION)
        redemption = self.get(F.REDEMPTION, face_amount)
        excoupon_period = self.get(F.EXCOUPON_PERIOD, ql.Period())
        excoupon_calendar = self.get(F.EXCOUPON_CALENDAR, ql.Calendar())
        excoupon_convention = self.get(F.EXCOUPON_DAY_CONVENTION, ql.Unadjusted)
        excoupon_end_of_month = self.get(F.EXCOUPON_END_OF_MONTH, False)

        bond = ql.FixedRateBond(
            settlement_days,
            face_amount,
            schedule,
            coupon,
            pay_basis,
            pay_convention,
            redemption,
            issue_date,
            pay_calendar,
            excoupon_period,
            excoupon_calendar,
            excoupon_convention,
            excoupon_end_of_month
        )
        return bond


class ZeroCouponBondCreator(CreatorBase):
    _templates = [T.INST_BOND_TBILL_HELPER, T.INST_BOND_TBILL]

    def _create(self, asof_date):
        settlement_days = self.get(F.SETTLEMENT_DAYS)
        face_amount = self.get(F.FACE_AMOUNT)
        maturity_date = self.get(F.MATURITY_DATE)
        issue_date = self.get(F.ISSUE_DATE) or self.get(F.ASOF_DATE) or asof_date
        pay_calendar = self.get(F.PAYMENT_CALENDAR)
        pay_convention = self.get(F.PAYMENT_DAY_CONVENTION) or self.get(F.ACCRUAL_DAY_CONVENTION)
        redemption = self.get(F.REDEMPTION, face_amount)

        bond = ql.ZeroCouponBond(
            settlement_days,
            pay_calendar,
            face_amount,
            maturity_date,
            pay_convention,
            redemption,
            issue_date
        )
        return bond