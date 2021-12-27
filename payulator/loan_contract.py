import pathlib as pl
from dataclasses import dataclass
from typing import Iterable, Optional
import tempfile
import subprocess as sp
import shutil
import json
import datetime as dt

import voluptuous as vt
import jinja2
import weasyprint as wp

from . import constants as cs
from .loan import Loan


@dataclass
class LoanContract(Loan):
    """
    Represents a loan contract.
    """

    date: str  # date of contract
    borrowers: Iterable[str]
    borrower_email: str
    securities: Optional[Iterable[str]] = None
    guarantors: Optional[Iterable[str]] = None
    notes: Optional[str] = None

    @classmethod
    def true_fields(cls) -> set[str]:
        """
        Return the set of names of LoanContract fields that are true fields and not
        init-only fields.
        """
        d = cls.__dataclass_fields__
        return {k for k in d if d[k].init}

    @staticmethod
    def validate(params: dict) -> dict:
        """
        Return the given loan contract parameters if they are valid.
        Otherwise raise a Voluptuous Invalid error.
        """
        # Loan keys
        Loan.validate({k: v for k, v in params.items() if k in Loan.true_fields()})
        # Remaining keys
        schema = vt.Schema(
            {
                "code": str,
                "date": dt.date,
                "borrowers": [str],
                "borrower_email": str,
                vt.Optional("securities"): vt.Any(None, list, [str]),
                vt.Optional("guarantors"): vt.Any(None, list, [str]),
                vt.Optional("notes"): vt.Any(None, str),
            },
            required=True,
        )
        schema({k: v for k, v in params.items() if k in schema.schema})

        return params

    def __post_init__(self):
        # Validate
        LoanContract.validate(self.__dict__)

        # Set defaults
        if self.securities is None:
            self.securities = []
        if self.guarantors is None:
            self.guarantors = []
        if self.notes is None:
            self.notes = ""

        # Derive 'kind' attributes
        self.set_kind()

    def to_rst(self, out_path: Optional[str] = None):
        """
        Return a RST version (string) of this loan contract.
        If a file path is given, then save to there instead.
        """
        # Set context dict
        a = {k: v for k, v in self.payments().items() if k != "payment_schedule"}
        if self.kind == "interest_only":
            loan_type = "interest-only"
        elif self.kind == "amortized":
            loan_type = "amortized"
        elif self.kind == "combination":
            loan_type = "interest-only then amortized"
        b = {
            "term": f"{self.num_payments} months",
            "term_interest_only": f"{self.num_payments_interest_only} months",
            "interest_rate_pc": f"{100*self.interest_rate}",
            "loan_type": loan_type,
        }
        context = self.__dict__ | a | b

        if self.kind == "amortized":
            template_path = cs.THEME_DIR / "amortized_loan_contract.rst"
        elif self.kind == "interest_only":
            template_path = cs.THEME_DIR / "interest_only_loan_contract.rst"
        elif self.kind == "combination":
            template_path = cs.THEME_DIR / "combination_loan_contract.rst"

        template_path = pl.Path(template_path)
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_path.parent)),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
            lstrip_blocks=True,
            trim_blocks=True,
        )
        template = env.get_template(str(template_path.name))
        rst = template.render(context)

        if out_path is not None:
            with pl.Path(out_path).open("w") as tgt:
                tgt.write(rst)

        else:
            return rst

    def to_html(self, out_path: Optional[str] = None) -> str:
        """
        Return an HTML version (string) of this contract.
        Use the RST version produced by :func:`to_rst` and rst2html5.py.
        If a file path is given, then save to there instead.
        """
        # Build RST and save to temp file
        with tempfile.TemporaryDirectory() as dirname:
            root = pl.Path(dirname)
            name = "contract"

            rst = self.to_rst()
            with (root / f"{name}.rst").open("w") as tgt:
                tgt.write(rst)

            args = [
                "rst2html5",
            ]

            stylesheet_paths = [
                cs.THEME_DIR / "css" / "bootstrap-4.3.1.min.css",
                cs.THEME_DIR / "css" / "style.css",
            ]
            for path in stylesheet_paths:
                arg = str(path.resolve())
                args.append(f"--stylesheet-inline={arg}")

            args.extend(
                [f"{name}.rst", f"{name}.html",]
            )

            cp = sp.run(
                args,
                cwd=str(root),
                universal_newlines=True,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
            )
            if cp.stderr:
                print("Failed:", cp.stderr)

            if out_path is not None:
                # Copy to out_path
                shutil.copy(root / f"{name}.html", pl.Path(out_path))

            else:
                with (root / f"{name}.html").open() as src:
                    html = src.read()

                return html

    @staticmethod
    def build_footer_css(footer_text):
        """
        Create a CSS string to place the given text in the left footer.
        """
        return f"""
            @page {{
                @bottom-left {{
                    content: "{footer_text}";
                }}
            }}
            """

    def to_pdf(self, out_path: Optional[str] = None):
        """
        Return a PDF version (string) of this loan contract.
        If a file path is given, then save to there instead.
        """
        # Put loan coad in footer
        stylesheets = [wp.CSS(string=LoanContract.build_footer_css(self.code))]

        with tempfile.NamedTemporaryFile() as fp:
            html_path = fp.name
            self.to_html(html_path)

            if out_path is not None:
                (
                    wp.HTML(filename=html_path).write_pdf(
                        pl.Path(out_path), stylesheets=stylesheets
                    )
                )
            else:
                (
                    wp.HTML(filename=html_path).write_pdf(
                        html_path, stylesheets=stylesheets
                    )
                )
                with pl.Path(html_path).open("rb") as src:
                    pdf = src.read()

                return pdf


def read_loan_contract(path: pl.PosixPath) -> "LoanContract":
    """
    Given a path to a JSON file encoding the attributes of an
    InterestOnlyLoan, AmortizedLoan, or CombinationLoan plus the the extra keys

    - ``'kind'`` indicating the kind of the loan
      (``'interest only'``, ``'amortized'``, or ``'combination'``),
    - the remaining attributes of a LoanContract

    do the following.
    Read the file, and return the corresponding validated LoanContract instance.
    Additional keys in the JSON file will be ignored.
    """
    with pl.Path(path).open() as src:
        params = json.load(src)

    # Parse some
    for key in ["date", "first_payment_date"]:
        if key in params:
            params[key] = dt.datetime.strptime(params[key], "%Y-%m-%d").date()

    # Prune parameters and validate
    pruned_params = LoanContract.validate(
        {k: v for k, v in params.items() if k in LoanContract.true_fields()}
    )

    return LoanContract(**pruned_params)
