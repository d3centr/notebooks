# Extracted Value

## Definitions

> Total Slippage = Pool Slippage + Block Slippage


- **Pool** Slippage (PS): the difference in expected output amount between the creation of a transaction (tx) and before its inclusion in a block, i.e. while *tx* is waiting in a pool. When a new transaction is included in the next block, PS = 0 because *tx* didn’t miss inclusion in any block (price wasn't updated). In general, the Pool Slippage of a transaction is the sum of all block slippages, excluding the last block where it is included.
```
                      Pool Slippage = 0
                      
           b                   b1                 b2
 
    blocks |-------------------|------------------|
                   ^           ^
                new tx   →    tx
                

                     Pool Slippage = b1 - b
                        
           b                   b1                b2
    blocks |-------------------|------------------|
                      ^                           ^
                   new tx      →                 tx
```

- **Block** Slippage (BS): the difference in output amount between the final state of last block and the position where a transaction is included in current block. BS captures the MEV value of a transaction. We often assume that it is extracted by block searchers, builders or validators and that it must be negative for the originating wallet. In fact, transactions have been ordered for as long as blocks and this measure not only includes MEV but also the expected slippage among transactions ordered by gas fees. We will have to identify front running in order to differentiate the cause of block slippage: is it determined by gas ranking or has it been influenced by a bot? Gas priority, latency, routing, MEV sequencing and arbitrage are some of block slippage causes.
```
        Block Slippage = t2 - t = log - trace

 tx call trace                           receipt log
       ^                                      ^
       t                   t1                 t2
   txs |-------------------|------------------|
                                              ^
                                              tx
 blocks -----------||----------------------------
             b                    b1
```
> transaction t is the final state of last block b

In our context, slippage exclusively refers to Block Slippage, some of it attributed to MEV.

## EV Calculation

1. The pre-block trace (call trace on previous block state) answers the question:\
*what would have been the outcome of this transaction if it had been placed first in the block?*
2. The receipt log answers the question:\
*what was the actual outcome of this transaction?*
3. The impact of sequencing can then be derived from the difference between 1 and 2. This gives us the Block Slippage. It can be calculated for any transaction.

BS is the primary indicator informing a receiving wallet whether the transaction experienced... 
- a *good* — Slippage > 0, positive Extracted Value — 
or 
- a *bad*  — Slippage < 0, negative Extracted Value — 
block sequencing.

Therefore, in the interest of better execution at all times, when not limited to intentional MEV:
> Block Slippage = Extracted Value (EV).

## EV Interpretation

When tx is a transaction with Extracted Value measured in a block...

- *EV < 0*: tx has incurred a loss due to front-running transactions
- *EV = 0*: no extracted value
- *EV > 0*: tx has been profitable back running transactions

Front runs and back runs do not have to be intentional. They simply mean that ordered outcomes of at least two transactions influenced each other. 