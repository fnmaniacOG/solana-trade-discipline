# Backtesting Honestly

A backtest exists to find out whether an edge is real *before* risking money — and its main job is to stop you from fooling yourself. Most backtests lie by being too optimistic. These rules keep them honest.

## Model the costs, or the result is fiction

- Subtract **realistic** swap fees, spread, slippage, and priority fees on every simulated trade — round trip. The biggest reason a "profitable" backtest loses live is costs that weren't modeled.
- The headline check: **is the average edge per trade bigger than the round-trip cost per trade?** If a strategy's edge is 0.4% and costs are 0.5%, it's a guaranteed slow loss no matter how good the win rate looks. Many "edges" are smaller than the spread and die on contact with reality.

## Don't overfit

- Split data: tune on **in-sample**, validate on untouched **out-of-sample**. A strategy that only works on the data you tuned it on works nowhere.
- Prefer **walk-forward** testing (roll the train/test window forward) over a single split.
- Be suspicious of strategies with many parameters or that only work in one regime. Fewer knobs = more likely real.
- A result that's *too* good is a red flag to hunt for a lookahead bug (using information the strategy couldn't have had at decision time), not a reason to celebrate.

## Sample size and honesty about variance

- A handful of winning trades proves nothing. You need enough trades that the result isn't luck — and even then, report the drawdown, not just the return.
- One vivid winning trade (or backtest) is not evidence. Survivorship and hindsight make losing strategies look great in memory — only the logged, costed sample tells the truth.

## Forward-test before you trust it

- After a backtest passes, **paper-trade or run it tiny live** before sizing up. Live fills, latency, and slippage differ from simulation; the forward test catches the gap.
- Track the same diagnostics live as in `exits.md` (win rate, payoff ratio, expectancy, adherence). If live materially underperforms the backtest, costs or execution are the usual culprit — find the leak before adding size.

## The mindset

A backtest's purpose is to *disconfirm* a strategy cheaply. Try to kill the idea with honest costs and out-of-sample data; if it survives that, *then* it's worth real money. An edge you can't measure, you can't trust — and "it felt like it worked" is not a measurement.
