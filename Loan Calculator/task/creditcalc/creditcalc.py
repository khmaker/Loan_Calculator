from argparse import ArgumentParser
from math import ceil, log


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--type', type=str)
    parser.add_argument('--principal', type=float)
    parser.add_argument('--periods', type=int)
    parser.add_argument('--interest', type=float)
    parser.add_argument('--payment', type=float)
    return parser.parse_args()


class LoanCalculator:

    def __init__(self, args):
        missing_type = args.type not in ('annuity', 'diff')
        missing_interest = args.interest is None
        missing_args = list(args.__dict__.values()).count(None) > 1
        parameter_is_negative = any(i < 0 for i in args.__dict__.values()
                                    if isinstance(i, (int, float)))
        if any((missing_type,
                missing_interest,
                missing_args,
                parameter_is_negative)):
            print('Incorrect parameters.')
            return
        self.type = args.type
        self.periods = args.periods
        self.principal = args.principal
        self.payment = args.payment
        self.nominal_interest_rate = args.interest / (12 * 100)
        self.payments = 0
        self.process_data()

    def process_data(self):
        if self.type == 'diff':
            return self.differentiated_payments()
        if self.periods is None:
            return self.number_of_payments()
        if self.principal is None:
            return self.loan_principal()
        if self.payment is None:
            return self.annuity_payment()

    def annuity_payment(self):
        """
        a = p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1))
        a = annuity payment;
        p = loan principal;
        i = nominal (monthly) interest rate;
        n = number of payments;
        """
        p = self.principal
        i = self.nominal_interest_rate
        n = self.periods
        a = ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
        print(f'Your annuity payment = {a}!')
        self.payment = ceil(a)
        self.payments = self.payment * self.periods
        self.overpayment()

    def number_of_payments(self):
        """
        n = log(a / (a - i * p), 1 + i)
        a = annuity payment;
        p = loan principal;
        i = nominal (monthly) interest rate;
        n = number of payments;
        """
        a = self.payment
        p = self.principal
        i = self.nominal_interest_rate
        n = ceil(log(a / (a - i * p), 1 + i))
        self.periods = n
        year, month = divmod(self.periods, 12)
        part1 = '{year} year{} '.format('s' if year > 1 else '',
                                        year=year)
        part2 = '{month} month{} '.format('s' if month > 1 else '',
                                          month=month)
        print('You need {}{}{}to repay this credit!'.format(
            part1 if year >= 1 else '',
            'and ' if (year and month) else '',
            part2 if month >= 1 else ''))
        self.payments = self.payment * self.periods
        self.overpayment()

    def loan_principal(self):
        """
        p = a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1))
        a = annuity payment;
        p = loan principal;
        i = nominal (monthly) interest rate;
        n = number of payments;
        """
        a = self.payment
        i = self.nominal_interest_rate
        n = self.periods
        p = ceil(a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
        self.principal = p
        print(f'Your credit principal = {self.principal}!')
        self.payments = self.payment * self.periods
        self.overpayment()

    def differentiated_payments(self):
        """
        dm = p / n + i ∗ (p − (p ∗ (m − 1)) / n)
        dm  = mth differentiated payment;
        p = the loan principal;
        i = nominal interest rate;
        n = number of payments;
        m = current repayment month.
        """
        p = self.principal
        i = self.nominal_interest_rate
        n = self.periods
        for m in range(1, n + 1):
            dm = ceil(p / n + i * (p - (p * (m - 1)) / n))
            print(f'Month {m}: paid out {dm}')
            self.payments += dm
        self.overpayment()

    def overpayment(self):
        overpayment = ceil(self.payments - self.principal)
        print(f'\nOverpayment = {overpayment}')


if __name__ == '__main__':
    loan_calculator = LoanCalculator(parse_arguments())
