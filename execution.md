# Execution Quality

A correct decision executed badly is a losing trade. On Solana specifically, the gap between the price you saw and the price you got — slippage, fees, MEV, failed transactions — can erase a real edge. Execution is where thin edges go to die.

## Slippage

- **Always set an explicit max-slippage** on every swap. Never send a market order with unbounded slippage on an illiquid token — that's how you buy the top of a sandwich.
- Size slippage tolerance to liquidity: tight (0.1–0.5%) for deep pairs, wider only when you've checked depth and accept it. If the required slippage to fill is large, the position is too big for the pool — cut size, don't widen tolerance.
- Quote against real routing (Jupiter) and compare expected-out to a reference price; if the deviation exceeds your threshold, abort.

## Priority fees & landing transactions

- Solana transactions need a **priority fee** (and often a **Jito tip**) to land reliably when the network is busy. A trade that doesn't land is worse than no trade — you think you're in/out and you're not.
- Set priority fee dynamically from recent network conditions, not a hardcoded constant. Cap it so fees never exceed a sane fraction of the trade's edge.
- For time-sensitive fills (snipes, exits), Jito bundles reduce the odds of being front-run.

## Confirmation, retries, partial fills

- **Confirm before you act on a fill.** Don't update position state until the transaction is finalized. Optimistically assuming a fill landed is a classic source of phantom positions.
- Build idempotent retries with fresh blockhashes — but never blindly resend a swap that may have already landed (you'll double your position). Check status first.
- Handle partial fills explicitly: know your actual filled size and recompute the stop/target against the real average entry, not the intended one.

## MEV / sandwich avoidance

- Public mempool swaps on illiquid tokens get sandwiched. Mitigate with: tight slippage caps, Jito bundles / private routing, and splitting large orders.
- Be especially careful on new/low-liquidity tokens — that's where sandwiching and honeypots concentrate. (Pair this with the kit's rug/safety check before trading such tokens at all.)

## The cost rule that ties back to the edge

Every trade pays: swap fee + spread + slippage + priority fee, round trip. Sum them. **If your expected edge is smaller than round-trip costs, there is no trade** — the edge is an illusion that execution will eat. Always evaluate net-of-cost R:R (see `backtesting.md`), and the cost estimate must be realistic, not optimistic.
