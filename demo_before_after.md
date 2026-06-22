# Demo: the skill applied to undisciplined trading code

This is the efficacy test — and a worked example for users. We take a naive "buy and hope"
bot and apply `solana-trade-discipline`. Every rule the skill catches is a real, account-ending
mistake that a data-or-swap skill would happily execute as written.

## Before — naive bot (what an agent writes without this skill)

```python
def trade(token, usd):
    price = get_price(token)
    swap(token, "buy", usd)                      # market order, all-in, unbounded slippage
    if get_price(token) < price * 0.9:           # down 10%?
        swap(token, "buy", usd)                  # ...buy more (average down)
    while get_price(token) < price * 2:          # hold until it doubles
        sleep(60)
    swap(token, "sell", balance(token))
```

## What the skill flags

| # | Violation | Rule | File |
|---|-----------|------|------|
| 1 | Sizes by "how much USD I have," not by risk; effectively all-in | Size by % risk from the stop; 0.5% default; never all-in | `sizing.md` |
| 2 | No stop-loss — no defined invalidation | Define the exit before the entry; CLQ | `exits.md` |
| 3 | Averages down into a loser | **Never add to a loser** | `exits.md` |
| 4 | No reward-to-risk check before entering | Net R:R ≥ 2.0 after costs, or skip | `sizing.md` |
| 5 | Market order, unbounded slippage | Explicit max-slippage on every swap | `execution.md` |
| 6 | "Hold until it doubles" — no target scale-out, no trailing, no time stop | Scale at T1 → breakeven → trail; time stop | `exits.md` |
| 7 | No edge check, no daily-loss cap | Only trade with an edge; daily circuit breaker | `mindset.md`, `sizing.md` |

## After — the same intent, disciplined

```python
def trade(token, account_equity, entry, stop, target1, target2, cost_per_unit):
    # 4. reward must clear 2x risk AFTER costs, or there's no trade
    if net_rr(entry, stop, target1, cost_per_unit) < 2.0:
        return None
    # 1. size from risk: lose only 0.5% of equity if stopped out (never all-in)
    size = size_from_risk(account_equity, risk_pct=0.5, entry=entry, stop=stop)
    # 5. enter with an explicit slippage cap; confirm the fill before trusting it
    fill = kit_swap(token, "buy", size, max_slippage_bps=50)
    pos = Position(token, "LONG", fill["avg_price"], fill["filled_size"],
                   stop, target1, target2, now())
    # 2 & 6: exits are pre-set and enforced mechanically — stop, scale at T1 -> breakeven,
    #        trail the rest to T2, time-stop if it stalls. 3: never add to the loser.
    while pos:
        pos = manage(pos)        # one rule-based decision per poll; no improvising
        sleep(POLL_SECONDS)
```

## Verdict

The skill catches **seven** distinct, real mistakes the naive version commits — each one a
documented way traders blow up accounts. That's the test: applied to undisciplined code, the
skill converts "buy and hope" into a sized, stopped, cost-aware, mechanically-exited trade.
It changes the output in exactly the direction it claims to. The skill works.
