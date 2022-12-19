
WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

# convert hexadecimal string to a decimal integer
#
def Ox(string):
    assert(string.startswith('0x'))
    if string == '0x':
        return 0
    else:
        return int(string, 16)
    
# Fill missing topics with a random address to keep clean equality conditions.
#
def randhex(size=40):
    result = []
    for _ in range(size):
        result.append(str(random.choice("0123456789ABCDEF")))
    # identify these strings with xx prefix
    return 'xx'+''.join(result)

def get_arbitrage_bots(flashes):
    arbitrage_bots = []
    for f in flashes:
        addresses = set()
        for swap in f.values():
            for a in [swap.entry.address, swap.exit.address]:
                addresses.add(a[-40:])
        arbitrage_bots.append(list(addresses))
    return arbitrage_bots

def read_eth(amount):
    return round(amount / 10**18, 3)

def eth_flow(trade, flash=False):
    if flash:
        if trade.exit.token == WETH:
            return (
                f'{read_eth(trade.exit.amount)}'
                f'/{read_eth(trade.entry.amount)}'
            )
        else:
            return '!= eth trade'
    else:
        if trade.exit.token == WETH:
            return f'{read_eth(trade.exit.amount)} out'
        elif trade.entry.token == WETH:
            return f'{read_eth(trade.entry.amount)} /in'
        else:
            return 'no eth'

def scan(b, print_arb=False):
    print(f'~ block {b} ~')
    block = load(b)
    
    # only ERC20 transfer events left in logs
    logs = [tx['receipt']['logs'] for tx in block]
    # propagate "from" address in case transfers go through a router
    pad = '0x000000000000000000000000'  # normalize with event topics
    origins = [pad + tx['receipt']['from'][-40:].lower() for tx in block]
    for i in range(len(block)):
        origin = origins[i]
        for l in logs[i]:
            l['origin'] = origin
            
    sandwiches = scan_sandwiches(logs)
    flashes = scan_arbitrages(logs)
    df = pd.DataFrame({
        'block': [b] * len(block),
        'transaction': [tx['tx']['hash'][2:] for tx in block], 
        'transfer': [len(log) > 0 for log in logs],
        'swap': has_swap(logs),
        'sandwich': [s is not None for s in sandwiches],
        'arbitrage': [len(f) > 0 for f in flashes]
    })
    
    arbitrage_bots = get_arbitrage_bots(flashes)
    bot, frontrun, backrun = [], [False]*len(block), [False]*len(block)
    for i, b in enumerate(arbitrage_bots):
        if len(b) == 1:
            bot.append(b[0])
        elif len(b) > 1:
            bot.append('mixed addresses')
        elif len(block) > i+1 and sandwiches[i+1] is not None:
            bot.append(sandwiches[i+1].exit.address[-40:])
            frontrun[i] = True
        elif sandwiches[i]:
            bot.append('n/a')
        elif i > 0 and sandwiches[i-1] is not None:
            bot.append(sandwiches[i-1].entry.address[-40:])
            backrun[i] = True
        else:
            bot.append(None)
    df['bot'] = [
        b[:12]+'..' if b is not None and b != 'n/a' else b 
        for b in bot
    ]
    
    df['tag'] = np.where(df['arbitrage'], 'arbitrage',
                np.where(df['sandwich'], 'sandwich',
                np.where(frontrun, 'frontrun',
                np.where(backrun, 'backrun',
                np.where(df['swap'], 'swap',
                np.where(df['transfer'], 'transfer', None))))))
    
    mev, eths = [], []
    for i, tag in enumerate(df.tag):
        
        if tag == 'frontrun':        
            mev.append('n/a')
            
            frontrun = sandwiches[i+1].swaps[0][0]
            eths.append(eth_flow(frontrun))
        
        elif tag == 'sandwich':       
            frontrun_price = sandwiches[i].swaps[0][0].xrate
            sandwich = sandwiches[i].swaps[0][1]
            sandwiched_price = sandwich.xrate
            diff = (frontrun_price - sandwiched_price) / frontrun_price * 100
            mev.append(round(diff, 2))
            
            eths.append(eth_flow(sandwich))
            
        elif tag == 'backrun':
            mev.append(round(sandwiches[i-1].pct, 2))
            
            backrun = sandwiches[i-1].swaps[0][2]
            eths.append(eth_flow(backrun))
            
        elif tag == 'arbitrage':
            arb = list(flashes[i].values())[0]
            mev.append(round(arb.pct, 2))
            eths.append(eth_flow(arb, flash=True))
            
        else:
            mev.append('n/a')
            eths.append('other')
            
    df['mev %'], df['eth'] = mev, eths
    
    output = df.loc[df['tag'].isin(['arbitrage', 'sandwich', 'frontrun', 'backrun']), 
        df.columns.difference(['transfer', 'swap', 'sandwich', 'arbitrage', 'block'])]
    
    if not output.empty:
        print(output.to_string())
        if print_arb:
            print('')
            for f in flashes:
                if f:
                    for swap in f.values():
                        swap.print() 
            for swap in sandwiches:
                if swap is not None:
                    swap.print()
    
    df['logs'], df['flashes'], df['sandwiches'] = logs, flashes, sandwiches
    return df
