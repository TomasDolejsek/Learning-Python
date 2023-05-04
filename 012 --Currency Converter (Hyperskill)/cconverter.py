currencies = {'RUB': 2.98, 'ARS': 0.82, 'HNL': 0.17, 'AUD': 1.9622, 'MAD': 0.208}
try:
    howmany = float(input())
    if howmany <= 0:
        raise ValueError
    for cur, val in currencies.items():
        print(f"I will get {howmany * val:.2f} {cur} from the sale of {howmany:.1f} conicoins.")
except ValueError:
    print("You should enter a number > 0")
