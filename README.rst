Payulator
***************
A Python 3.9+ package to compute loan payments, make loan contracts, etc. for Merriweather.
Inspired by the business loan calculator at `Calculator.net <https://www.calculator.net/business-loan-calculator.html>`_.


Installation
============
``poetry add git+ssh://git@gitlab.com/merriweather/payulator``


Usage
=====
Play with the examples in the Jupyter notebook at ``notebooks/examples.ipynb``.


Authors
=======
- Alex Raichev, 2018-01-20


Documentation
=============
Will publish on Gitlab `here <https://araichev.gitlab.io/payulator_docs/>`_.


Changes
=======

2.0.4, 2024-06-23
-----------------
- Fixed slicing in ``helpers.aggregate_payment_schedules``.
- Updated dependencies.
- Improved testing imports.

2.0.3, 2024-02-08
-----------------
- Replaced 'monthly' in contract templates with payment frequency of loan contract.
- Updated dependencies and tested with Python 3.11.

2.0.2, 2022-05-24
-----------------
- Updated tax notebook.


2.0.1, 2021-01-03
-----------------
- Corrected bank account number in loan contracts.


2.0.0, 2021-12-28
-----------------
- Major refactor.
- Added a notebook to email payment schedules.


1.0.0, 2021-11-25
-----------------
- First release based on previous work.
