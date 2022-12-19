import plotly.graph_objects as go

Oxd4e9_labels = {
    '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2': 'ETH',
    '0x39AD1AA1f898bA5681D40d0d6AF123596519b712': 'SBF',
    '01ff6318440f7d5553a82294d78262d5f5084eff': 'Bot',
    '7a250d5630b4cf539739df2c5dacb4c659f2488d': 'Uniswap V2: Router 2',
    '2eed3903103383999c00ab2c74cf8a28336c49af': 'Uniswap V2: SBF 32',
    'bef893c409048a6d032746caa24ad9b6ef5b23a9': 'Victim',
    'extra': [{
        'source': 'bef893c409048a6d032746caa24ad9b6ef5b23a9',
        'target': '7a250d5630b4cf539739df2c5dacb4c659f2488d',
        'token': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    }]
}

def draw_pure_sandwich(df, link_extra=True, by_tx=False, LABELS={}):
    pool = df[df.sandwich].sandwiches.values[0].swaps[0][1].inflows[0].fo
    trimmed_pool = pool[-40:]
    
    outflow_flags = df.logs.apply(lambda logs: pool in [l['topics'][1] for l in logs])
    inflow_flags = df.logs.apply(lambda logs: pool in [l['topics'][2] for l in logs])
    sdf = df[outflow_flags | inflow_flags].copy()
    sdf['outflows'] = sdf.logs.apply(lambda logs: [(l['topics'][2][-40:], l['address'], l['data']) 
                                                    for l in logs if l['topics'][1] == pool])
    sdf['inflows'] = sdf.logs.apply(lambda logs: [(l['topics'][1][-40:], l['address'], l['data']) 
                                                   for l in logs if l['topics'][2] == pool])
    
    inflow_counts = sdf.inflows.apply(len)
    outflow_counts = sdf.outflows.apply(len)
    pure = (
        list(inflow_counts.unique()) == [1] and 
        list(outflow_counts.unique()) == [1] and
        len(inflow_counts == 3) and 
        len(outflow_counts == 3)
    )
    if pure:
        
        outflow_addresses = sdf.outflows.apply(lambda flows: flows[0][0])
        inflow_addresses = sdf.inflows.apply(lambda flows: flows[0][0])
        outflow_tokens = sdf.outflows.apply(lambda flows: flows[0][1])
        inflow_tokens = sdf.inflows.apply(lambda flows: flows[0][1])
        
        TAGS = [
            'Frontrun', 'Sandwich', 'Backrun', 
            'Bot 1', 'Victim', ' Bot 2',  # add space before Bot 2 to order by tx
            'Pool 1', 'Pool 2', 'Pool 3'
        ]
        labels = set(
            TAGS + 
            [trimmed_pool] +
            list(outflow_addresses) + 
            list(inflow_addresses)
        )
        lookup = {label: i for i, label in enumerate(labels)}
        labels = [LABELS.get(l, l) for l in list(labels)]
        if by_tx:
            source_suffix = [lookup[t] for t in ['Frontrun', 'Sandwich', 'Backrun']]
            target_prefix = [lookup[t] for t in ['Bot 1', 'Victim', ' Bot 2']]
            pool_series = [lookup[t] for t in ['Pool 1', 'Pool 2', 'Pool 3']]
        else:
            source_suffix = [lookup[i] for i in inflow_addresses]
            target_prefix = [lookup[o] for o in outflow_addresses]
            pool_series = [lookup[trimmed_pool]] * len(outflow_addresses)
            
        source = pool_series + source_suffix
        target = target_prefix + pool_series
        add_flow = link_extra and len(LABELS.get('extra', [])) > 0
        if add_flow:
            for e in LABELS['extra']:
                source.append(lookup[e['source']])
                target.append(lookup[e['target']])
        # not using amounts (which would have to be normalized on the same scale...):
        # reflect number of transfers in width instead
        link_value = [1] * len(target)
        extra_tokens = [e['token'] for e in LABELS['extra']] if add_flow else []
        link_label = [
            LABELS.get(l, l) 
            for l in list(outflow_tokens) + list(inflow_tokens) + extra_tokens
        ]
        COLORS = ['blue', 'orange', 'green', 'purple']
        color_lookup = {l: COLORS[i] for i, l in enumerate(set(link_label))}
        link_color = [color_lookup[l] for l in link_label]
            
        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(color = "black", width = 0.5),
                label = labels,
                color = "black"
            ),
            link = dict(
                source = source,
                target = target,
                value = link_value,
                label = link_label,
                color = link_color
        ))])
        
        fig.update_layout(
            title_text = 'Typical Pattern of a Sandwich Attack', 
            font_size = 10,
        )
        fig.show()
        
    else:
        print('Noisy transactions found in block: cannot draw a pure pattern.')