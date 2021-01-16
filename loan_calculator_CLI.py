import argparse
import math


def correct_parameters():
    count_arg = 0
    for k in range(len(arguments)):
        if arguments[k] is not None:
            count_arg += 1

    if args.type not in ['annuity', 'diff'] or \
            count_arg != 4 or \
            args.interest is None or \
            (args.type == 'diff' and args.payment is not None) or \
            (args.principal or args.payment or args.periods or args.interest) < 0:
        return False


def calculate_differentiated_payments():
    P = args.principal
    n = args.periods
    i = args.interest / 100 / 12  # convert loan interest to nominal interest rate
    d = []
    total_payments = 0

    for m in range(1, n + 1):
        diff_payment = math.ceil(P / n + i * (P - P * (m - 1) / n))
        d.append(diff_payment)
        print(f'Month {m}: payment is {d[m - 1]}')
        total_payments += d[m - 1]

    overpayment = round(total_payments - P)

    print(f'\nOverpayment = {overpayment}')


def calculate_annuity_payment():
    P = args.principal
    n = args.periods
    i = args.interest / 100 / 12  # convert loan interest to nominal interest rate

    a = P * i * pow(1 + i, n) / (pow(1 + i, n) - 1)
    a = math.ceil(a)
    overpayment = round(a * n - P)

    print(f'Your annuity payment = {a}!')
    print(f'Overpayment = {overpayment}')


def calculate_principal():
    A = args.payment
    n = args.periods
    i = args.interest / 100 / 12  # convert loan interest to nominal interest rate

    P = math.floor(A / (i * pow(1 + i, n) / (pow(1 + i, n) - 1)))
    overpayment = round(A * n - P)

    print(f'Your loan principal = {P}!')
    print(f'Overpayment = {overpayment}')


def calculate_number_of_periods():
    P = args.principal
    A = args.payment
    i = args.interest / 100 / 12

    n = math.log(A / (A - i * P), 1 + i)
    n = math.ceil(n)

    num_years = n // 12
    num_months = n % 12
    year_str = 'years' if num_years > 1 else 'year'
    month_str = 'months' if num_months > 1 else 'month'

    if num_years == 0:
        print(f'It will take {num_months} {month_str} to repay this loan!')
    elif num_months == 0:
        print(f'It will take {num_years} {year_str} to repay this loan!')
    else:
        print(f'It will take {num_years} {year_str} and {num_months} {month_str} to repay this loan!')

    overpayment = round(A * n - P)
    print()
    print(f'Overpayment = {overpayment}')


parser = argparse.ArgumentParser(description="This is a real loan calculator!")

parser.add_argument("-t", "--type")
parser.add_argument("-p", "--principal", type=float)
parser.add_argument("-a", "--payment", type=float)
parser.add_argument("-n", "--periods", type=int)
parser.add_argument("-i", "--interest", type=float)

args = parser.parse_args()

arguments = [args.type, args.principal, args.payment, args.periods, args.interest]

if correct_parameters() is False:
    print('Incorrect parameters')
    exit()
else:
    if args.type == 'diff':
        calculate_differentiated_payments()
    if args.type == 'annuity' and args.payment is None:
        calculate_annuity_payment()
    if args.type == 'annuity' and args.principal is None:
        calculate_principal()
    if args.type == 'annuity' and args.periods is None:
        calculate_number_of_periods()
