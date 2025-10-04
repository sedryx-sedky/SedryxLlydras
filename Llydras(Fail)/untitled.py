import Llydras as ly

def value(p, prices):
    return {t : round(float(prices.now[t] * sh), 2) for t, sh in p.holdings.items()}

def f(xs):
    if xs == '': return {}
    xs = xs.replace(' ', '')
    ys = [x.split(':') for x in xs.split(',')]
    zs = {y[0].upper() : float(y[1]) for y in ys}
    return zs

def g(p, orders):
    for t, q in orders.items():
        if q >= 0:
            p.buy(t, q)
        else:
            p.sell(t, -q)

p = ly.Portfolio(['AAPL', 'JPM', 'GOOG'])
T = p.assets
p.deposit(1000)
for date, prices in p.trade('2024-01-01', '2024-01-5'):
    v = {t : round(float(prices.now[t]), 2) for t in T}
    k = value(p, prices)
    print(f'–––––––––{date}–––––––––')
    print(f'Cash: {p.balance}')
    print(f'Asset Prices: {v}')
    print(f'Holdings: {k}')
    print(f'Portfolio Value(without cash): {sum(k.values())}')
    j = input('Orders> ')
    g(p, f(j))

p._date = date
u = prices.data.loc[date]

print('Closing all position')
g(p, {t : -(sh * u[t]) for t, sh in p.holdings.items()})
p._date = None
print(f'Cash: {p.balance}')