# Position Sizing

Sizing is decided *before* the trade and *from the stop* — never by gut, never "how much do I feel like." Get this right and a string of losers is survivable; get it wrong and one trade ends the account.

## The default: fixed-fractional risk

Risk a fixed, small fraction of the **account** per trade — not a fixed dollar amount, not a fixed token count.

```
risk_dollars   = account_equity * risk_pct          # default risk_pct = 0.5%–1%
risk_per_unit  = abs(entry_price - stop_price)       # what you lose per token if stopped
position_size  = risk_dollars / risk_per_unit        # in tokens
notional       = position_size * entry_price
```

The key consequence: **a wider stop produces a smaller position, not more risk.** Stop distance and size move together so dollars-at-risk stay constant. This is what makes risk consistent across very different setups.

## Volatility-aware (ATR) sizing

For noisy tokens, set the stop a multiple of ATR away so normal volatility doesn't stop you out, then size from that distance:

```
stop_distance = atr_multiple * ATR        # e.g. 1.5 * ATR
position_size = (account_equity * risk_pct) / stop_distance
```

Higher-volatility tokens automatically get smaller positions. Lower-vol get larger. Risk stays flat.

## Half-Kelly (optional, for measured edges)

If you have a *measured* edge and payoff (from backtests, not vibes), Kelly gives the growth-optimal fraction:

```
f = (b*p - q) / b      # b = payout ratio, p = win prob, q = 1-p
```

Always use **half-Kelly or less.** Full Kelly assumes your probabilities are exact (they never are) and produces stomach-churning drawdowns. If the edge isn't measured, don't use Kelly — fall back to fixed-fractional.

## Reward-to-risk floor

**Take no trade whose reward isn't at least 2× its risk — measured *net of costs.*** A 2:1 net R:R means you can be wrong more than half the time and still come out ahead, which is the whole point of an edge. Reward smaller than 2× the risk (after fees + slippage) doesn't clear the bar — skip it. (This is stricter than a 1.5× floor on purpose: on Solana, costs and slippage eat thin setups, so the gross number has to be generous to leave 2× *net.*)

## Hard caps (enforce regardless of the above)

- **Per-trade risk:** **0.5% of equity is the default.** Go up toward 1% only for your highest-confidence, *measured*-edge setups — never on a hunch.
- **Daily-loss circuit breaker:** stop trading for the day at **−5% of equity** (= 10× the default per-trade risk, i.e. ~10 losing trades). This is a *behavioral* guardrail against tilt and revenge-trading, not a sizing rule. It's set wide enough that normal variance won't trip it, tight enough that a genuinely bad day stops you. Active scalpers can run wider; 2-trades-a-day swing traders should run tighter — frequency drives it.
- **Strategic circuit breaker:** if you hit the daily cap **2–3 days in a row, halt entirely and review the strategy** — don't just trade again tomorrow. Repeatedly tripping the daily stop means the edge is gone or you're off your process; ten straight max-loss days is −40%, and you should be stopped and diagnosing long before then.
- **Total open risk:** sum of all open positions' risk ≤ ~3–5% of equity.
- **Correlation cap:** positions that move together (same narrative, same sector, same beta) count as **one** bet for the exposure cap. Three correlated longs is one position's worth of conviction, not three.
- **Single-token cap:** no one token exceeds a set % of the book, no matter how good it looks.

## Reminders

- Size from the account's *current* equity, not its peak — risk shrinks with the account, which is what stops a drawdown from compounding.
- Never increase size to "make back" a loss. That's the martingale road to zero.
- Free/bonus capital is still capital — size it the same way once it's yours to lose.
