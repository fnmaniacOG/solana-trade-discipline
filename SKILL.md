---
name: solana-trade-discipline
description: Use when building, reviewing, or hardening a Solana trading bot or strategy. Covers position sizing, stop-loss / take-profit / trailing exits and scale-outs, portfolio risk limits, and slippage / priority-fee / MEV-aware execution. This is the risk-management and exit-discipline layer that data and swap skills do not provide — invoke it whenever code places, sizes, or manages a trade on Solana.
---

# Solana Trade Discipline

Most Solana trading tools answer "what's the price?" and "how do I swap?" Almost none answer the questions that actually decide whether a strategy makes or loses money: **how much do I buy, where do I get out, and how do I execute without bleeding the edge away.** This skill is that missing layer — the judgment a system needs once it can already fetch data and place orders.

The core principle, learned the expensive way: **entries are easy and cheap; exits and sizing are where accounts are made and lost.** A bot with a mediocre entry and disciplined exits beats a bot with a great entry and no exit plan, every time. This skill encodes that discipline so an agent building a trading system doesn't ship the second kind.

## When to use this skill

Invoke this whenever the task involves a Solana trade being **placed, sized, or managed** — building a trading bot, a sniper, a copy-trader, an arbitrage loop, a DCA system, or reviewing/auditing existing trading code for risk. If code calls a swap (Jupiter), opens a perp (Drift), or holds a position, this skill applies.

## The non-negotiables (apply to every trade)

1. **Size by risk, never by gut.** Decide the dollars-at-risk *before* the trade, as a fixed fraction of the account. Never "feel out" a size. → `sizing.md`
2. **Define the exit before the entry.** Stop, target(s), and invalidation are set at entry and enforced mechanically (a resting order, not a human watching). You do not improvise exits mid-trade. → `exits.md`
3. **Never widen a stop.** Moving a stop further away to avoid being wrong is the single most account-ending habit. The stop only ever moves *toward* profit (to breakeven, then trailing).
4. **Cut losers fast, let winners run.** The fatal leak is the opposite — small wins, big losses. Track average win vs average loss; if avg loss > avg win, the strategy bleeds even with a >50% hit rate. → `exits.md`
5. **Net the costs.** Fees, spread, slippage, and priority fees are real. An edge smaller than round-trip costs is not an edge. Always evaluate R:R *after* costs. → `execution.md`, `backtesting.md`
6. **Cap total exposure.** Per-trade risk AND portfolio risk (correlated positions count as one bet). One bad correlated cluster shouldn't be able to halve the account.
7. **Discipline over prediction.** Trade only with an edge, never revenge-trade, never override the plan mid-trade, and track every trade so the data — not the memory — tells the truth. The leaks are behavioral, and they recur. → `mindset.md`

## Pre-trade checklist (run before any order goes live)

- [ ] Position sized to a fixed % risk of account (default 0.5–1%)?
- [ ] Stop price set, and is it a real invalidation level (not an arbitrary %)?
- [ ] Target(s) set, with a plan to scale out and move stop to breakeven?
- [ ] Net R:R (after fees + slippage) ≥ 2.0? If not, skip the trade.
- [ ] Slippage limit and priority-fee strategy set for execution?
- [ ] Does this position correlate with open positions? If so, does combined risk still fit the cap?
- [ ] Is the exit enforced by a resting/limit order, not by intending to watch it?

If any box is unchecked, the trade is not ready.

## How this fits the rest of the Solana AI Kit

This skill is the **judgment layer on top of the kit's existing primitives** — it does not replace them, it directs them:

- **Data** (Pyth, DexPaprika, Nansen) → feeds the sizing and exit calculations.
- **Execution** (Jupiter swaps, Drift perps) → the hands this skill tells where to act, at what size, with what slippage guard.
- **Security skills** (audit/rug) → answer "is this token safe?"; this skill answers "given it's tradeable, how do I trade it without blowing up?"

## Reference files (load as needed)

- **`sizing.md`** — position sizing: % risk per trade, ATR-based, fixed-fractional, half-Kelly; max exposure and correlation caps.
- **`exits.md`** — the heart of the skill: stop-loss, take-profit, trailing stops, scale-outs, time stops, move-to-breakeven, and the cut-losers/let-winners-run discipline.
- **`execution.md`** — slippage limits, priority fees / Jito, retries and confirmation, partial fills, and avoiding sandwich/MEV.
- **`backtesting.md`** — backtesting honestly: modeling fees and slippage, avoiding overfitting, and the "is the edge bigger than the cost?" check.
- **`reference/risk_managed_trade.py`** — a runnable example of a full risk-managed trade lifecycle (size → enter → set stop/target → manage exit) wired to the kit's price and swap primitives.
