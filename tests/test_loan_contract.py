import json
import datetime as dt
from copy import copy

import pytest
import voluptuous as vt

from .context import payulator, DATA_DIR
import payulator as pl


def test_validate():
    with (DATA_DIR / "good_loan_contract_params.json").open() as src:
        params = json.load(src)

    for key in ["date", "first_payment_date"]:
        if key in params:
            params[key] = dt.datetime.strptime(params[key], "%Y-%m-%d").date()

    pl.LoanContract.validate(params)

    p = copy(params)
    p["fee"] = "whoops"
    with pytest.raises(vt.MultipleInvalid):
        pl.LoanContract.validate(p)

    p = copy(params)
    p["interest_rate"] = -1
    with pytest.raises(vt.MultipleInvalid):
        pl.LoanContract.validate(p)

    p = copy(params)
    p["first_payment_date"] = "2018-03-21"
    with pytest.raises(vt.MultipleInvalid):
        pl.LoanContract.validate(p)


def test_true_fields():
    assert pl.LoanContract.true_fields() == {
        "code",
        "principal",
        "interest_rate",
        "payment_freq",
        "compounding_freq",
        "num_payments",
        "num_payments_interest_only",
        "fee",
        "first_payment_date",
        "date",
        "borrowers",
        "borrower_email",
        "securities",
        "guarantors",
        "notes",
    }


def test_read_loan_contract():
    path = DATA_DIR / "good_loan_contract_params.json"
    loan = pl.read_loan_contract(path)
    assert isinstance(loan, pl.LoanContract)

    path = DATA_DIR / "bad_loan_contract_params.json"
    with pytest.raises(vt.MultipleInvalid):
        pl.read_loan_contract(path)
