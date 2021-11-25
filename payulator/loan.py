"""
Module defining the Loan class.
"""
import pathlib as pl
import numbers
import json
import datetime as dt
from typing import Union, Literal
from dataclasses import dataclass, field

import pandas as pd
import numpy as np
import voluptuous as vt

from . import constants as cs
from . import helpers as hp


@dataclass
class Loan:
    """
    A base class for different kinds of loans.
    Uses the other classes.
    Attributes are

    - ``code``: code name for the loan; defaults to a
      timestamp-based code
    - ``kind``: kind of loan; 'amortized', 'interest_only', or 'combination'
    - ``principal``: amount of loan, that is, the principal
    - ``interest_rate``: nominal annual interest rate
      (not as a percentage), e.g. 0.1 for 10%
    - ``payment_freq``: payments frequency;
      one of the keys of :const:`NUM_BY_FREQ`, e.g. 'monthly'
    - ``compounding_freq``: compounding frequency;
      one of the keys of :const:`NUM_BY_FREQ`, e.g. 'monthly';
      defaults to ``payment_freq``
    - ``num_payments``: number of payments in the loan
      term
    - ``num_payments_interest_only``: number of initial interest only payments
      in the loan term; possibly 0 or ``num_payments``
    - ``fee``: loan fee
    - ``first_payment_date``: date object; date of first loan
      payment

    """

    code: str
    principal: float
    interest_rate: float
    payment_freq: str
    compounding_freq: str
    num_payments: int
    num_payments_interest_only: int
    fee: float
    first_payment_date: dt.date
    # Derived attributes
    kind: Literal["interest_only", "amortized", "combination"] = field(init=False)

    @staticmethod
    def validate(params: dict) -> dict:
        """
        Check the given dictionary of Loan init attributes,
        skipping non-init attributes.
        Return the input if it is valid.
        Otherwise, raise a Voluptuous Invalid error.
        """

        def check_pos(value):
            if isinstance(value, numbers.Number) and value > 0:
                return value
            raise vt.Invalid("Not a positive number")

        def check_nneg(value):
            if isinstance(value, numbers.Number) and value >= 0:
                return value
            raise vt.Invalid("Not a nonnegative number")

        def check_pos_int(value):
            if isinstance(value, int) and value > 0:
                return value
            raise vt.Invalid("Not a positive integer")

        def check_freq(value):
            if value in cs.NUM_BY_FREQ:
                return value
            raise vt.Invalid(f"Frequncy must be one of {cs.NUM_BY_FREQ.keys()}")

        schema = vt.Schema(
            {
                "code": str,
                "principal": check_pos,
                "interest_rate": check_nneg,
                "payment_freq": check_freq,
                "compounding_freq": check_freq,
                "num_payments": check_pos_int,
                "num_payments_interest_only": check_nneg,
                "first_payment_date": dt.date,
                "fee": check_nneg,
            },
            required=True,
        )

        params = schema(params)

        # Extra checks
        if params["num_payments_interest_only"] > params["num_payments"]:
            raise vt.Invalid(
                "Number of interest only payments cannot exceed number of payments"
            )

        return params

    @classmethod
    def true_fields(cls) -> set[str]:
        """
        Return the set of names of Loan fields that are true fields and not
        init-only fields.
        """
        d = cls.__dataclass_fields__
        return {k for k in d if d[k].init}

    def set_kind(self) -> None:
        """
        Set the ``kind`` attribute of this loan, which involves comparing
        the two attributes ``num_payments`` and ``num_payments_interest_only``.
        """
        if self.num_payments_interest_only == 0:
            self.kind = "amortized"
        elif self.num_payments_interest_only == self.num_payments:
            self.kind = "interest_only"
        else:
            self.kind = "combination"

    def __post_init__(self) -> None:
        Loan.validate(self.__dict__)
        self.set_kind()

    def copy(self) -> "Loan":
        """
        Return a copy of this Loan.
        """
        return Loan(self.__dict__)

    def interest_only_part(self) -> Union[None, "Loan"]:
        """
        Return a new Loan representing the interest only part of this loan.
        Return None if there is no interest only part.
        """
        if self.kind == "amortized":
            return None

        attrs = {k: getattr(self, k) for k in Loan.true_fields()}

        # Correct some attributes
        attrs["num_payments"] = self.num_payments_interest_only

        return Loan(**attrs)

    def amortized_part(self) -> Union[None, "Loan"]:
        """
        Return a new Loan representing the amortized part of this loan.
        Return None if there is no amortized part.
        """
        if self.kind == "interest_only":
            return None

        attrs = {k: getattr(self, k) for k in Loan.true_fields()}

        # Correct some attributes
        if self.num_payments_interest_only > 0:
            attrs["fee"] = 0
        attrs["num_payments"] = self.num_payments - self.num_payments_interest_only
        attrs["num_payments_interest_only"] = 0
        date_offset = hp.to_date_offset(hp.freq_to_num(self.payment_freq))
        attrs["first_payment_date"] = (
            pd.Timestamp(self.first_payment_date)
            + self.num_payments_interest_only * date_offset
        ).date()

        return Loan(**attrs)

    def payments(self, decimals: int = 2) -> dict:
        """
        Create a payment schedule etc. for this Loan.
        Return a dictionary with the following keys and values.

        - ``"payment_schedule"``: DataFrame; schedule of loan payments
          broken into principal payments and interest payments
        - ``"periodic_payment"``: the monthly payment in case of an interest only or
          amortized loan; in case of a combination loan, a dictionary with the keys
          'interest_only' and 'amortized' with values the corresponding periodic payments
          of the interest only and amortized loan parts, respectively
        - ``"interest_total"``: total interest paid on loan
        - ``"interest_and_fee_total"``: interest total plus loan fee
        - ``"payment_total"``: total of all loan payments, including the
          loan fee
        - ``"interest_and_fee_total_over_principal``: interest_and_fee_total_over_principal
        - ``"first_payment_date"``
        - ``"last_payment_date"``

        Round all values to the given number of decimal places, but do not
        round if ``decimals is None``.

        The payment schedule has the columns:

        - ``"payment_sequence"``: integer
        - ``"payment_date"``
        - ``"beginning_balance"``: float; balance on the payment date before the principal
          payment is made
        - ``"principal_payment"``: float; principal payment made on payment date
        - ``"ending_balance"``: float; balance on the payment date after the principal
          payment is made
        - ``"interest_payment"``: float; interest payment made on payment date
        - ``"fee_payment"``: float; fee payment made on payment date; equals the fee on
          the first payment date and 0 elsewhere
        - ``"total_payment"``: float; fee_payemnt + principal_payment + interest_payment
        - ``"notes"``: NaN

        """
        if self.kind == "interest_only":
            k = hp.freq_to_num(self.payment_freq)
            A = self.principal * self.interest_rate / k
            n = self.num_payments
            f = (
                pd.DataFrame({"payment_sequence": range(1, n + 1)})
                .assign(beginning_balance=self.principal)
                .assign(principal_payment=0)
                .assign(ending_balance=self.principal)
                .assign(interest_payment=A)
                .assign(fee_payment=0)
            )
            f.principal_payment.iat[-1] = self.principal
            f.ending_balance.iat[-1] = 0
            f.fee_payment.iat[0] = self.fee
            f["total_payment"] = (
                f.fee_payment + f.principal_payment + f.interest_payment
            )
            f["notes"] = np.nan

            date_offset = hp.to_date_offset(k)
            if date_offset:
                # Kludge for pd.date_range not working easily here;
                # see https://github.com/pandas-dev/pandas/issues/2289
                f["payment_date"] = [
                    pd.Timestamp(self.first_payment_date) + j * date_offset
                    for j in range(n)
                ]
                # Put payment date first
                cols = f.columns.tolist()
                cols.remove("payment_date")
                cols.insert(1, "payment_date")
                f = f[cols].copy()

            # Bundle result into dictionary
            d = {}
            d["payment_schedule"] = f
            d["periodic_payment"] = A
            d["interest_total"] = f["interest_payment"].sum()
            d["interest_and_fee_total"] = d["interest_total"] + self.fee
            d["payment_total"] = d["interest_and_fee_total"] + self.principal
            d["interest_and_fee_total_over_principal"] = (
                d["interest_and_fee_total"] / self.principal
            )
            if "payment_date" in f:
                d["first_payment_date"] = f.payment_date.iat[0].date()
                d["last_payment_date"] = f.payment_date.iat[-1].date()

        elif self.kind == "amortized":
            A = hp.amortize(
                self.principal,
                self.interest_rate,
                self.compounding_freq,
                self.payment_freq,
                self.num_payments,
            )
            p = hp.build_principal_fn(
                self.principal,
                self.interest_rate,
                self.compounding_freq,
                self.payment_freq,
                self.num_payments,
            )
            n = self.num_payments
            f = (
                pd.DataFrame({"payment_sequence": range(1, n + 1)})
                .assign(beginning_balance=lambda x: (x.payment_sequence - 1).map(p))
                .assign(
                    principal_payment=lambda x: x.beginning_balance.diff(-1).fillna(
                        x.beginning_balance.iat[-1]
                    )
                )
                .assign(
                    ending_balance=lambda x: x.beginning_balance - x.principal_payment
                )
                .assign(interest_payment=lambda x: A - x.principal_payment)
                .assign(fee_payment=0)
            )
            f.fee_payment.iat[0] = self.fee
            f["total_payment"] = (
                f.fee_payment + f.principal_payment + f.interest_payment
            )
            f["notes"] = np.nan

            date_offset = hp.to_date_offset(hp.freq_to_num(self.payment_freq))
            if date_offset:
                # Kludge for pd.date_range not working easily here;
                # see https://github.com/pandas-dev/pandas/issues/2289
                f["payment_date"] = [
                    pd.Timestamp(self.first_payment_date) + j * date_offset
                    for j in range(n)
                ]
                # Put payment date first
                cols = f.columns.tolist()
                cols.remove("payment_date")
                cols.insert(1, "payment_date")
                f = f[cols].copy()

            # Bundle result into dictionary
            d = {}
            d["payment_schedule"] = f
            d["periodic_payment"] = A
            d["interest_total"] = f["interest_payment"].sum()
            d["interest_and_fee_total"] = d["interest_total"] + self.fee
            d["payment_total"] = d["interest_and_fee_total"] + self.principal
            d["interest_and_fee_total_over_principal"] = (
                d["interest_and_fee_total"] / self.principal
            )
            d["first_payment_date"] = f.payment_date.iat[0].date()
            d["last_payment_date"] = f.payment_date.iat[-1].date()

        else:
            # Combination loan
            iops = self.interest_only_part().payments(decimals=None)
            aps = self.amortized_part().payments(decimals=None)

            # Combine payment schedules
            f_io = iops["payment_schedule"].copy()
            f_io["principal_payment"].iat[-1] = 0
            f_io["ending_balance"].iat[-1] = self.principal
            f_io["total_payment"].iat[-1] -= self.principal
            f_a = aps["payment_schedule"]
            f = (
                pd.concat([f_io, f_a])
                .reset_index(drop=True)
                .assign(payment_sequence=lambda x: x.index + 1)
            )

            # Combine other items
            d = {}
            d["payment_schedule"] = f
            d["periodic_payment"] = {
                "interest_only": iops["periodic_payment"],
                "amortized": aps["periodic_payment"],
            }
            d["interest_total"] = f["interest_payment"].sum()
            d["interest_and_fee_total"] = d["interest_total"] + self.fee
            d["payment_total"] = d["interest_and_fee_total"] + self.principal
            d["interest_and_fee_total_over_principal"] = (
                d["interest_and_fee_total"] / self.principal
            )
            d["first_payment_date"] = {
                "interest_only": iops["first_payment_date"],
                "amortized": aps["first_payment_date"],
            }
            d["last_payment_date"] = {
                "interest_only": iops["last_payment_date"],
                "amortized": aps["last_payment_date"],
            }
        if decimals is not None:
            for key, val in d.items():
                if isinstance(val, pd.DataFrame):
                    d[key] = val.round(decimals)
                elif isinstance(val, dict):
                    try:
                        d[key] = {k: round(v, decimals) for k, v in val.items()}
                    except TypeError:
                        continue
                elif isinstance(val, float):
                    d[key] = round(val, decimals)

        return d


def read_loan(path: pl.PosixPath) -> "Loan":
    """
    Given a path to a JSON file encoding the true attributes of a Loan
    (excluding init-only attributes), read the file, and
    return the corresponding validated Loan instance.
    Additional keys in the JSON file will be ignored.
    """
    with pl.Path(path).open() as src:
        params = json.load(src)

    # Parse date
    if "first_payment_date" in params:
        params["first_payment_date"] = pd.to_datetime(
            params["first_payment_date"]
        ).date()

    # Prune parameters and validate
    pruned_params = Loan.validate(
        {k: v for k, v in params.items() if k in Loan.true_fields()}
    )

    return Loan(**pruned_params)
