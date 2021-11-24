import pytest

from .context import merriweather_py, DATA_DIR
from merriweather_py import *


def test_validate():
    params = {
        "code": "test-20180324",
        "principal": 10000,
        "interest_rate": 0.12,
        "num_payments": 6,
        "num_payments_interest_only": 2,
        "payment_freq": "monthly",
        "compounding_freq": "continuously",
        "first_payment_date": dt.date(2018, 3, 24),
        "fee": 250,
    }
    Loan.validate(params)

    p = copy(params)
    p["fee"] = "whoops"
    with pytest.raises(vt.MultipleInvalid):
        Loan.validate(p)

    p = copy(params)
    p["interest_rate"] = -1
    with pytest.raises(vt.MultipleInvalid):
        Loan.validate(p)

    p = copy(params)
    p["first_payment_date"] = "2018-03-24"
    with pytest.raises(vt.MultipleInvalid):
        Loan.validate(p)


def test_true_fields():
    assert Loan.true_fields() == {
        "code",
        "principal",
        "interest_rate",
        "payment_freq",
        "compounding_freq",
        "num_payments",
        "num_payments_interest_only",
        "fee",
        "first_payment_date",
    }


def test_set_kind():
    loan = Loan(
        code="",
        principal=1000,
        interest_rate=0.05,
        payment_freq="monthly",
        compounding_freq="quarterly",
        num_payments=3 * 12,
        num_payments_interest_only=12,
        fee=10,
        first_payment_date=dt.date(2018, 1, 1),
    )
    assert loan.kind == "combination"

    loan.num_payments_interest_only = 0
    loan.set_kind()
    assert loan.kind == "amortized"

    loan.num_payments_interest_only = loan.num_payments
    loan.set_kind()
    assert loan.kind == "interest_only"


def test_interest_only_part():
    loan = Loan(
        code="",
        principal=1000,
        interest_rate=0.05,
        payment_freq="monthly",
        compounding_freq="quarterly",
        num_payments=3 * 12,
        num_payments_interest_only=12,
        fee=10,
        first_payment_date=dt.date(2018, 1, 1),
    )
    io_loan = loan.interest_only_part()
    assert isinstance(io_loan, Loan)
    for k, v in io_loan.__dict__.items():
        if k == "kind":
            assert v == "interest_only"
        elif k == "num_payments":
            assert v == getattr(loan, "num_payments_interest_only")
        else:
            assert v == getattr(loan, k)


def test_amortized_part():
    loan = Loan(
        code="",
        principal=1000,
        interest_rate=0.05,
        payment_freq="monthly",
        compounding_freq="quarterly",
        num_payments=3 * 12,
        num_payments_interest_only=12,
        fee=10,
        first_payment_date=dt.date(2018, 1, 1),
    )
    a_loan = loan.amortized_part()
    assert isinstance(a_loan, Loan)
    for k, v in a_loan.__dict__.items():
        if k == "kind":
            assert v == "amortized"
        elif k == "fee":
            assert v == 0
        elif k == "num_payments":
            assert v == loan.num_payments - loan.num_payments_interest_only
        elif k == "num_payments_interest_only":
            assert v == 0
        elif k == "first_payment_date":
            assert v == dt.date(2019, 1, 1)
        else:
            assert v == getattr(loan, k)


def test_summarize():
    # Interest only
    loan = Loan(
        code="",
        principal=100,
        interest_rate=0.12,
        payment_freq="monthly",
        compounding_freq="monthly",
        num_payments=12,
        num_payments_interest_only=12,
        fee=13,
        first_payment_date=dt.date(2018, 1, 1),
    )
    s = loan.summarize()
    expect_keys = {
        "payment_schedule",
        "periodic_payment",
        "interest_total",
        "interest_and_fee_total",
        "payment_total",
        "interest_and_fee_total_over_principal",
        "first_payment_date",
        "last_payment_date",
    }
    assert set(s.keys()) == expect_keys
    assert round(s["interest_and_fee_total"], 2) == 25
    assert isinstance(s["first_payment_date"], dt.date)
    assert isinstance(s["last_payment_date"], dt.date)


    # Check payment schedule
    f = s["payment_schedule"]
    assert set(f.columns) == {
        "payment_sequence",
        "payment_date",
        "beginning_balance",
        "principal_payment",
        "ending_balance",
        "interest_payment",
        "fee_payment",
        "total_payment",
        "notes",
    }
    assert f.shape[0] == 12
    assert (f["interest_payment"] == 1).all()
    assert (f["principal_payment"].iloc[:-1] == 0).all()
    assert f["principal_payment"].iat[-1] == 100

    # Amortized
    loan = Loan(
        code="",
        principal=1000,
        interest_rate=0.05,
        payment_freq="monthly",
        compounding_freq="quarterly",
        num_payments=3 * 12,
        num_payments_interest_only=0,
        fee=10,
        first_payment_date=dt.date(2018, 1, 1),
    )
    s = loan.summarize()
    assert set(s.keys()) == {
        "payment_schedule",
        "periodic_payment",
        "interest_total",
        "interest_and_fee_total",
        "payment_total",
        "interest_and_fee_total_over_principal",
        "first_payment_date",
        "last_payment_date",
    }
    assert round(s["periodic_payment"], 2) == 29.96
    assert round(s["interest_and_fee_total"], 2) == 88.62
    assert isinstance(s["first_payment_date"], dt.date)
    assert isinstance(s["last_payment_date"], dt.date)

    # Check payment schedule
    f = s["payment_schedule"]
    assert set(f.columns) == {
        "payment_sequence",
        "payment_date",
        "beginning_balance",
        "principal_payment",
        "ending_balance",
        "interest_payment",
        "fee_payment",
        "total_payment",
        "notes",
    }
    assert f.shape[0] == 3 * 12
    f["payment"] = f["interest_payment"] + f["principal_payment"]
    assert (abs(f["payment"] - 29.96) <= 0.015).all()

    # Combination
    loan = Loan(
        code="",
        principal=1000,
        interest_rate=0.05,
        payment_freq="monthly",
        compounding_freq="quarterly",
        num_payments=4 * 12,
        num_payments_interest_only=12,
        fee=10,
        first_payment_date=dt.date(2018, 1, 1),
    )
    s = loan.summarize()
    # Check non-payment schedule items
    assert set(s.keys()) == {
        "payment_schedule",
        "periodic_payment",
        "interest_total",
        "interest_and_fee_total",
        "payment_total",
        "interest_and_fee_total_over_principal",
        "first_payment_date",
        "last_payment_date",
    }
    iops = loan.interest_only_part().summarize()
    aps = loan.amortized_part().summarize()
    assert set(s["periodic_payment"].keys()) == {"interest_only", "amortized"}
    assert s["interest_and_fee_total"] == (
        iops["interest_and_fee_total"] + aps["interest_and_fee_total"]
    )
    assert set(s["first_payment_date"].keys()) == {"interest_only", "amortized"}
    assert set(s["last_payment_date"].keys()) == {"interest_only", "amortized"}

    # Check payment schedule
    f = s["payment_schedule"]
    assert set(f.columns) == {
        "payment_sequence",
        "payment_date",
        "beginning_balance",
        "principal_payment",
        "ending_balance",
        "interest_payment",
        "fee_payment",
        "total_payment",
        "notes",
    }
    assert f.shape[0] == 4 * 12


def test_read_loan():
    path = DATA_DIR / "good_loan_params.json"
    loan = read_loan(path)
    assert isinstance(loan, Loan)

    path = DATA_DIR / "bad_loan_params.json"
    with pytest.raises(vt.MultipleInvalid):
        read_loan(path)
