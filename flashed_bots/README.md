# Flashed Bots

> measuring and detecting MEV slippage

## Background

Since the release of Flashboys 2.0 [paper](https://arxiv.org/pdf/1904.05234.pdf) in 2019, MEV, the value created by the ordering of transactions in a block, has been a hot topic. Bots taking advantage of latency and information asymmetries to extract MEV operate in the [dark](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest). Better visibility on extracted value (EV) in block sequencing empowers all parties interacting with programmable blockchains. Suboptimal block inclusion and positioning opportunities must be detected to execute more favorable transactions. Flashed Bots is an attempt to define a full coverage of EV measurement in a finalized block.

## Approach

Flashbots has opened source [mev-inspect](https://github.com/flashbots/mev-inspect-py) to address the issue and [zeromev](https://zeromev.org/) expanded on it to include sandwich attacks. The strength of Flashbots solution lies in a design with modular, protocol specific, inspectors, providing detailed information within its coverage. On the other hand, Flashed Bots is exploring a synthesis of MEV analytics: an all-encompassing metric. Trading off protocol details for full coverage in a generic and protocol-agnostic method delivers a standard indicator of frictional payments. It complements the story told by gas fees to better reflect the financial reality of every transaction.

*We propose Block Slippage to measure and detect the extraction of MEV.*

- definition in [Extracted Value](Extracted_Value.md)
- [Data Collection](Data_Collection.md)
- test run Analysis (notebook *coming soon*)

---

*Illuminate bots in the block!*
![](images/flashed_bots.jpeg)