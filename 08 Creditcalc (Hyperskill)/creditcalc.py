import argparse, math

def number_of_payments(P, A, i):
    i /= 1200
    n = math.ceil(math.log(A / (A - i * P), 1 + i))
    years = math.floor(n / 12)
    months = math.ceil(n - years * 12)
    if months == 12:
        years += 1
        months = 0
    
    print("It will take ", end = '')
    if years > 0:
        print(f"{years} year{'s' if years > 1 else ''}{' and' if months > 0 else ''} ", end ='')
    if months > 0:
        print(f"{months} month{'s' if months > 1 else ''} ",end = '')
    print("to repay this loan!")
    return round(A * n - P)

def ordinary_annuity(P, n, i):
    i /= 1200
    A = math.ceil(P * ((i * ((1 + i) ** n)) / ((1 + i) ** n - 1)))
    print(f"Your annuity payment = {A}!")
    return round(A * n - P)

def loan_principal(A, n, i):
    i /= 1200
    P = math.floor(A / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
    print(f"Your loan principal = {P}!")
    return round(A * n - P)
    
def differentiated_payment(P, n, i):
    i /= 1200
    paid = 0
    for m in range(1, n + 1):
        D = math.ceil((P / n) + i * (P - (P * (m - 1) / n)))
        paid += D
        print(f"Month {m}: payment is {D}")
    print()
    return round(paid - P)

def check_arguments(values):
    if values.count(None) != 1:  # too few or too many parameters
        return False
    if values[0] == 'diff' and values[2] != None:  # diff with wrong parameters
        return False
    for value in values[1:]:
        if value is not None and value <= 0:  # value is negative
            return False
    return True

# main program
parser = argparse.ArgumentParser(description = "Loan Calculator")
parser.add_argument('--type', choices = ['annuity','diff'])
parser.add_argument('--principal', type = float)
parser.add_argument('--payment', type = float)
parser.add_argument('--periods', type = int)
parser.add_argument('--interest', type = float)

args = parser.parse_args()
arglist = list(vars(args).values())  # list of input values

if not check_arguments(arglist):
    print("Incorrect parameters.")
    exit()
           
if args.type == 'annuity':
    if not args.principal:
        print(f"Overpayment = {loan_principal(args.payment, args.periods, args.interest)}")
    elif not args.payment:
        print(f"Overpayment = {ordinary_annuity(args.principal, args.periods, args.interest)}")
    elif not args.periods:
        print(f"Overpayment = {number_of_payments(args.principal, args.payment, args.interest)}")
else:
    print(f"Overpayment = {differentiated_payment(args.principal, args.periods, args.interest)}")