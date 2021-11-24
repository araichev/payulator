LOAN AGREEMENT
***************

**Date** {{ date }} · **Contract Code** {{ code }}


Parties
========
The Borrower has requested that the Lender makes the Loan available to the Borrower.
The Lender has agreed to make available the Loan to the Borrower on the terms and conditions set out in this Agreement.

- **Lender**: Merriweather Limited (NZCN 6762055, NZBN 9429046653192)
- **Borrower(s)**: {{ borrowers|join('; ') }}
- **Guarantor(s)**: {{ guarantors|join('; ') }}


Loan Terms
================

.. class:: table table-striped table-condensed table-bordered
.. list-table::
    :widths: 1 3
    :header-rows: 0

    * - **Drawdown Date**
      - The date of the signing of this agreement
    * - **Loan Amount**
      - {{ "{:,.0f}$".format(principal) }}
    * - **Loan Type**
      - {{ loan_type.capitalize() }}
    * - **Term**
      - {{ term }}
    * - **Annual Interest Rate**
      - {{ interest_rate_pc }}%
    * - **Total Interest Charges**
      - {{ "{:,.2f}$".format(interest_total) }}
    * - **Administration Fee**
      - {{ "{:,}$".format(fee) }}
    * - **Total Amount of Payments**
      - {{ "{:,.2f}$".format(payment_total) }}
    * - **Method of Calculating Interest**
      - Interest charges are calculated by multiplying the unpaid balance of the loan amount at the end of the day by a daily interest rate equal to the Annual Interest Rate divided by 365. Interest is charged monthly.
    * - **Payment Schedule**
      - {{ num_payments }} consecutive monthly payments of {{ "{:,.2f}$".format(periodic_payment) }} begining on {{ first_payment_date }} and ending on {{ last_payment_date }} plus one payment of {{ "{:,.0f}$".format(principal) }} on {{ last_payment_date }}. The Administration Fee is deducted from the Loan Amount on the Drawdown Date
    * - **Payment Account**
      - All payments must be made to the Kiwibank bank account of Merriweather Limited at 38-9019-0508016-00
    * - **Default Interest Rate**
      - The Annual Interest Rate plus 10%
    * - **Securities**
      {% if securities %}
      -
        {% for security in securities %}
        - {{ security }}
        {% endfor %}
      {% endif %}


.. class:: pagebreak


Signatures
===========

- Alexander Raichev, Director of Merriweather Limited:           _______________________________________

  Signed in the presence of

  Witness signature:            _______________________________________

  Witness name:                 _______________________________________

  Witness occupation:           _______________________________________

  Witness town of residence:    _______________________________________



{% if guarantors %}
  {% for guarantor in guarantors %}


- {{ guarantor }}: _______________________________________

  Signed in the presence of

  Witness signature:            _______________________________________

  Witness name:                 _______________________________________

  Witness occupation:           _______________________________________

  Witness town of residence:    _______________________________________

  {% endfor %}
{% else %}
  {% for borrower in borrowers %}


- {{ borrower }}: _______________________________________

  Signed in the presence of

  Witness signature:            _______________________________________

  Witness name:                 _______________________________________

  Witness occupation:           _______________________________________

  Witness town of residence:    _______________________________________

  {% endfor %}
{% endif %}


.. class:: pagebreak

General Terms
==============

1. Agreement and Drawdown of the Loan
--------------------------------------
1.1 This Agreement consists of the Loan Terms and these General Terms. In the case of any conflict between the Loan Terms and these General Terms, the Loan Terms will prevail.

1.2 The Loan will be drawn down by the Borrower in one sum on the Drawdown Date, unless otherwise agreed by the Lender. Further instalments of the Loan may be drawn down by the Borrower as agreed in writing by the Lender and each such draw down will be subject to the terms of this Agreement.


2. Security
------------
2.1 The Borrower agrees and covenants with the Lender to provide the Security. The Borrower agrees that the Lender has been granted a security interest which it may register on the Personal Property Security Register.

2.2 The Borrower agrees to give any further Security as the Lender may from time to time require.

2.3 On or before the Drawdown Date the Borrower shall execute such documentation as the Lender deems necessary to give effect to the Security. The Security, and any further Security as the Lender may from time to time require, shall be in the form required by the Lender.

2.4 The Borrower shall comply with all of the Borrower’s obligations under each Security, and any such further Security as the Lender may require from time to time.


3. Term and Repayment
----------------------
3.1 The Loan will be for the Term so specified in the Loan Terms.

3.2 Subject to earlier termination in accordance with this Agreement, the Borrower must repay the Loan to the Lender together with interest according to the Payment Schedule.

3.3 If, in accordance with the Loan Terms, interest is payable on the Loan, interest on the Loan will be payable as set out in the Payment Schedule.


4. Payments
------------
4.1 All sums payable by the Borrower to the Lender under this Agreement must be:

    4.1.1 Paid no later than 15:00 on the due date or otherwise in the manner and at the times agreed upon between the Lender and the Borrower;

    4.1.2 Paid for value when due in immediately available funds; and

    4.1.3 Be paid free and clear of any restriction, stipulation or condition and without any set-off or deduction whatsoever (other than as required by law).

4.2 If any due date for a payment is not a Business Day, payment will be made on the next Business Day.

4.3 If the Borrower is required by law to make any deduction or withholding from any sum payable to the Lender the amount due from the Borrower will be increased to the extent necessary to ensure that, after making that deduction or withholding, the Lender receives on the relevant due date a net sum equal to the amount which it would have received had there been no such deduction or withholding.

4.4 The Lender may, without prior notice or demand, set-off or reduce any obligation (of any type and on any account whatsoever) that it has to the Borrower, against any sum or obligation or debt payable by the Borrower to the Lender (whether under this Agreement or not and whether such liability is actual or contingent, primary or collateral, joint or several). The Lender may exercise its rights under this clause irrespective of whether or not payment by the Borrower is due to the Lender under this Agreement.

4.5 If the Borrower does not make any payment (including a payment of interest) due under this Agreement on the due date, the Borrower must pay interest at the Default Interest Rate on the payment due and any other amounts payable pursuant to this Agreement (both before and after judgment) for the period from the due date until the actual date of payment. Default Interest will accrue daily, and will be compounded monthly and will itself be added to and form part of the Loan, provided that the capitalisation of unpaid interest in accordance with this clause will not prejudice the Lender’s rights and remedies in respect of unpaid interest being a default under this Agreement. This clause is without prejudice to any other rights and remedies of the Lender.


5. Undertakings
-----------------
5.1 The Borrower undertakes that it will:

    5.1.1 Promptly give written notice to the Lender of the occurrence of any Event of Default or potential Event of Default immediately on becoming aware of it, and provide full details of any action taken (or to be taken) as a result;

    5.1.2 Promptly give notice to the Lender of the occurrence of any event or circumstance which may have a material adverse effect on it;

    5.1.3 Promptly apply for and obtain renewals of all leases, licences and authorities which may be necessary or expedient for carrying on its business;

    5.1.4 Pay and discharge when due all rates, taxes, assessments and outgoings payable by it, and all other debts and liabilities payable by it;

    5.1.5 Comply with its obligations under this Agreement and each of the Security and all laws and regulatory requirements;

    5.1.6 Promptly give the Lender written notice of any change in its address, electronic mail address or facsimile number; and

    5.1.7 Insure and keep insured in the manner and amounts required by the Lender and by the applicable insurer advised by the Lender (if so advised) and otherwise for full replacement, all assets of the Borrower and any other insurances the Lender may require.

5.2 The Borrower undertakes that it will not, except with the prior written consent of the Lender:

    5.2.1 Create or permit to subsist any security interest over any of its assets except any created or permitted by this Agreement;

    5.2.2 Sell, transfer or otherwise dispose of any of its assets, except for value in the ordinary course of business;

    5.2.3 Make any loan or provide any financial assistance to any director, shareholder or associated or related person or, except in the ordinary course of business, lend or advance moneys to any other person; or

    5.2.4 Enter into any other transaction with, or for the benefit of, a related person except on arms’ length commercial terms.


6. Charges, Costs, and Expenses
--------------------------------
6.1 The Borrower will pay to the Lender upon demand an amount equal to all costs, losses, expenses, and other liabilities on a full indemnity basis (including legal expenses and goods and services and similar taxes thereon) incurred or sustained by the Lender in connection with:

    6.1.1 The release of this Agreement;

    6.1.2 The exercise, enforcement or preservation, or attempted exercise, enforcement or preservation, of any right under this Agreement, or in suing for or recovering any amount owing under this Agreement; and

    6.1.3 The granting of any waiver or consent under, or the giving of any variation or release of, this Agreement.


7. Early Repayment
---------------------
7.1 The Borrower may pay the Loan or any portion of it early.
If the Borrower chooses to pay early the Borrower must still pay the Total Interest Charges.

7.2 Any amount paid early will not be available for reborrowing unless otherwise agreed by the Lender.


8. Events of Default
----------------------
8.1 An Event of Default is deemed to occur if, at any time and for any reason, whether or not within the control of a party, any of the following events occur:

    8.1.1 The Borrower fails to pay on its due date any amount payable under this Agreement;

    8.1.2 The Borrower fails to comply with any of its other obligations under this Agreement or under the Security provided that, in the case of a failure that is capable of remedy, that failure is not remedied to the satisfaction of the Lender within ten Business Days of the date that the Borrower first became aware of it;

    8.1.3 Any representation or warranty made by the Borrower, or any information provided by the Borrower in connection with this Agreement or the Security to the Lender is untrue in any material respect or is or proves to have been untrue or misleading in any material respect when made or repeated;

    8.1.4 This Agreement or any of the Security ceases to be in full force and effect or its validity or enforceability is contested by any person (other than the Lender);

    8.1.5 A person (other than the Lender) repudiates, or does anything evidencing an intention to repudiate, this Agreement or any of the Security;

    8.1.6 The Borrower:

        a. is insolvent or unable to pay its debts as they fall due or, if the Borrower is a company, is deemed to be so under the terms of the Companies Act 1993;

        b. stops or suspends payment of any of its debts or threatens to do so; or

        c. makes, or proposes to make, any compromise, assignment, arrangement or composition with, or for the benefit of, its creditors;

    8.1.7 A distress, attachment, execution or other legal process is levied against any of the Borrower’s assets or a judgment of any court against the Borrower remains unsatisfied for more than five Business Days;

    8.1.8 A receiver, trustee, manager, administrator or similar officer is appointed in respect of the Borrower or any of its property;

    8.1.9 The Borrower ceases or threatens to cease to carry on the Borrower’s business, or, if the Borrower is a company, any step is taken or proposal made to dissolve or amalgamate the Borrower;

    8.1.10 It becomes illegal for the Borrower or any other person to comply with its obligations under this Agreement or any of the Security, or all or any part of any such document becomes invalid or unenforceable;

    8.1.11 If the Borrower is other than a natural person:

        a. a material change occurs in the control, ownership or management of the Borrower without the prior written consent of the Lender; or

        b. an order is made requiring the Borrower or any of its subsidiaries to pay any debts of another entity; or

        c. an order is made, resolution passed or other step taken by a person for the liquidation of the Borrower, except for the purpose of and followed by a reconstruction or reorganisation (not involving or arising out of insolvency) on terms approved by the Lender before that step is taken; or

        d. any step is taken, or recommendation made, to appoint a statutory manager under the Corporations (Investigation and Management) Act 1989 in respect of the Borrower or any of its subsidiaries; or

        e. any step is taken by the shareholders of the Borrower to adopt a constitution or alter the constitution of the Borrower in a manner that could, in the opinion of the Lender, adversely affect the interests of the Lender;

    8.1.12 In the opinion of the Lender, any event occurs which may have a material adverse change effect in relation to the Borrower or any subsidiary of the Borrower; or

    8.1.13 A security interest in property of the Borrower becomes enforceable; or

    8.1.14 If the financial position of the Borrower shall deteriorate materially from that disclosed in any previous financial statements of the Borrower disclosed to the Lender,

8.2 If an Event of Default occurs the Lender may, at any time thereafter by notice in writing to the Borrower:

    8.2.1 declare its obligations under this Agreement to be terminated, and declare the Loan, all interest due on the Loan and all other amounts payable under this Agreement to be immediately due and payable; and

    8.2.2 appoint a receiver of all or any of the assets of the Borrower. The Lender may remove any receiver and may appoint a new receiver in place of any receiver who has been removed, retired or died.


9. Notices
------------
9.1 Any notice given pursuant to this Agreement will be deemed to be validly given if either:

    9.1.1 Personally delivered; or

    9.1.2 Sent by electronic means (commonly known as email),
    to the address or email address of the party last used by the notifying party or as the party to be notified may designate by written notice given to the other party.

9.2 Any notice given pursuant to this Agreement will be deemed to be validly given:

    9.2.1 In the case of delivery, when received;

    9.2.2 In the case of electronic transmission by email, at the time specified in the email transmission which was not returned as undeliverable or as containing any error.

9.3 If the delivery or transmission of any notice given under this Agreement is on a day which is not a Business Day, or occurs after 17:00 (local time) on any Business Day, the notice will be deemed to be received on the next following day which is a Business Day.


10. Assignment
---------------
10.1 The Lender may assign and transfer all or any of its rights and obligations under this Agreement to any person or persons.

10.2 The Lender may disclose, on a confidential basis, to a potential assignee or transferee or other person to which contractual relations in connection with this Agreement are contemplated, any information about the Borrower or the Guarantor.

10.3 Neither the Borrower nor the Guarantor may assign any of its rights or obligations under this Agreement without the prior written consent of the Lender.


11. General
-------------
11.1 The Borrower will pay the Lender’s reasonable legal costs related to the preparation and negotiation of this Agreement. Time is of the essence under this Agreement.

11.2 If at any time any provision of this Agreement is or becomes illegal, invalid or unenforceable in any respect, that illegality, invalidity or unenforceability will not affect the enforceability of the provisions of this Agreement.

11.3 No delay, failure or forbearance by a party to exercise (in whole or in part) any right, power or remedy under, or in connection with this Agreement will operate as a waiver of such right, power or remedy, nor will any single or partial exercise of any such right, power or remedy preclude any other or future exercise of the same, or any other right, power or remedy under this Agreement.

11.4 The Lender's right to payment of any Indebtedness (including under any negotiable instrument or agreement) will not merge in the Borrower's obligation to pay the Loan under this Agreement. The Lender has no duty to marshal in favour of the Borrower or any other person.

11.5 The rights, powers, and remedies provided in this Agreement are in addition to, and not exclusive of, any rights, powers or remedies provided by law. The Lender may give or withhold any approval or consent in its absolute discretion, and either conditionally or unconditionally.

11.6 This Agreement will be governed by, and construed in accordance with, the laws of New Zealand, and the parties hereby submit to the exclusive jurisdiction of the courts of New Zealand.

11.7 This Agreement may be executed and exchanged in any number of counterparts (including copies, facsimile copies, and scanned email copies) each of which is to be deemed an original, but all of which together are to constitute a binding and enforceable agreement between the parties.


12. Definitions and Interpretation
-------------------------------------
12.1 In addition to the terms defined in the Loan Terms, in this Agreement, unless the context requires otherwise:

     - **Agreement** means this agreement and includes any appendices and/or schedules attached to it.

     - **Business Day** means a day which is not a Saturday, Sunday or public holiday in Auckland.

     - **Event of Default** means the occurrence of any event specified in clause 8.

     - **Indebtedness** means all indebtedness of the Borrower to the Lender or incurred by the Lender on behalf of the Borrower (including all interest, costs, taxes, stamp or similar duties or taxes, commissions, charges, and expenses (including legal fees and expenses) incurred or sustained in any way by the Lender in connection with that indebtedness or the enforcement or attempted enforcement of that indebtedness under this Loan Agreement.

     - **Loan** means the total amount advanced by the Lender to the Borrower as specified in the Loan Terms and includes all obligations (whether present or future but other than obligations to pay money) of the Borrower to the Lender under this Loan Agreement.

12.2 In this Agreement, unless the context otherwise requires:

    12.2.1 The term including means "including without limitation".

    12.2.2 The terms written and in writing include any means of reproducing words, figures or symbols in a tangible and visible form.

    12.2.3 A reference to the opinion, satisfaction or discretion of the  Lender or where a matter is required to be acceptable to the Lender,  that opinion, satisfaction, discretion, acceptability or determination is in the sole and absolute discretion of the Lender.

    12.2.4 Expressions defined in the main body of this Agreement have the  defined meaning in the whole of the Agreement, including the  background.

    12.2.5 Reference to a party will include that party’s executors,  administrators, successors and permitted assignees or transferees.

    12.2.6 Any obligation not to do anything will be deemed to include an  obligation not to suffer, permit or cause that thing to be done.
