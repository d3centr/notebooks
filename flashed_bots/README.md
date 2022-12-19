# Flashed Bots

> detecting & measuring MEV

Token swaps create potential for MEV, the theoretical total value extracted from the ordering of transactions, as a side effect of their execution. Smart contract intermediations of token exchanges generate price differentials, which are captured by the fastest and most prioritized bots. We propose Block Slippage, which includes the spread of arbitrage and sandwiches, to measure MEV extraction: definition in [Extracted Value](Extracted_Value.md).

1. initial [Data Collection](eda/Data_Collection.md)
2. MEV scanner & sandwich attacks in a Python [Analysis](eda/Analysis.ipynb)
3. *coming soon* - Flashlight, a block analyzer

## Background

Since the release of Flashboys 2.0 [paper](https://arxiv.org/pdf/1904.05234.pdf) in 2019, MEV has been a hot topic. Bots taking advantage of latency and information asymmetries to extract MEV operate in the [dark](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest). Better visibility on extracted value (EV) in block sequencing empowers all parties interacting with programmable blockchains. Suboptimal block inclusion must be detected to execute more favorable transactions. Flashed Bots is an attempt to define a full coverage of EV measurement in a finalized block.

## Approach

Flashbots has opened source [mev-inspect](https://github.com/flashbots/mev-inspect-py) to address the issue and [zeromev](https://zeromev.org/) expanded on it to include sandwich attacks. The strength of Flashbots solution lies in a design with modular, protocol specific, inspectors, providing detailed information within its coverage. On the other hand, Flashed Bots is exploring a synthesis of MEV analytics. Trading off protocol details for full coverage in a generic and protocol-agnostic method delivers standard indicators. They complete the story told by gas fees to understand frictional payments and opportunities in every transaction.

> Wallets extracting the MEV of their own transactions have the potential to make DeFi trading free. Shedding more light on Extracted Value will help reach a new level of efficiency that could outcompete legacy structures.

---

*Illuminate bots in the block!*
![](images/flashed_bots.jpeg)
