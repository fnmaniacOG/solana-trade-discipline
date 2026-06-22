# solana-trade-discipline

A Claude Code / AI-assistant **skill** that gives Solana trading agents the one thing the rest of the kit doesn't: **judgment.** Position sizing, exit discipline, risk limits, and cost-aware execution — the layer that decides *how much to buy, where to get out, and how to execute without bleeding the edge away.*

## The problem it solves

Every trading tool in the Solana ecosystem answers "what's the price?" (Pyth, DexPaprika, Nansen) and "how do I swap/open a position?" (Jupiter, Drift). **None of them answer the questions that actually decide whether a strategy makes or loses money:**

- How much do I risk on this trade?
- Where's my stop, and where do I take profit?
- Is the reward worth the risk *after* fees and slippage?
- When do I stop for the day so a bad run doesn't become a blown account?

An agent can fetch perfect data and fire a flawless swap and still go to zero, because it has no risk management or exit discipline. This skill is that missing layer — built from rules paid for in real losses, not theory.

## What's the gap (novelty)

Checked against the kit's `skill-registry.json`: the catalog is **data + execution**, with no *discipline* layer. Rug/security risk is covered (Trail of Bits, GhostSecurity); *trading* risk — sizing, stops, exits, R:R, execution quality — is not. This skill fills that gap, and it's cross-domain: the discipline applies to any trading agent (DeFi, perps, sniping, copy-trading, arb), not one protocol.

## What's inside

Progressive-loading: `SKILL.md` stays lean and routes to a pillar only when needed.

| File | Covers |
|------|--------|
| `SKILL.md` | Entry point: non-negotiables, pre-trade checklist, routing |
| `sizing.md` | % risk per trade (0.5% default), ATR/half-Kelly, 2× net R:R floor, daily + strategic circuit breakers, exposure & correlation caps |
| `exits.md` | Stops, take-profits, trailing, scale-outs, time stops, move-to-breakeven; cut-losers/let-winners-run |
| `execution.md` | Slippage caps, priority fees / Jito, confirmation & retries, partial fills, MEV/sandwich avoidance |
| `backtesting.md` | Modeling fees+slippage, avoiding overfitting, the edge-vs-cost check, forward-testing |
| `mindset.md` | Discipline & probabilistic-thinking rules (no revenge trades, plan adherence, edge-only) |
| `reference/risk_managed_trade.py` | Runnable reference: size → enter → set stop/target → manage exit, with offline-testable pure logic |
| `reference/demo_before_after.md` | Worked example: the skill applied to an undisciplined bot, catching 7 real mistakes |

## Install

Drop it into a Claude Code project's skills directory:

```bash
# as a submodule (matches how the kit catalogs external skills)
git submodule add https://github.com/fnmaniacOG/solana-trade-discipline \
  .claude/skills/ext/solana-trade-discipline

# — or simply copy the folder into .claude/skills/
```

Then add an entry to the kit's `.claude/skills/skill-registry.json` (see the PR). The skill auto-loads when a task involves placing, sizing, or managing a Solana trade.

## Tested

- `python reference/risk_managed_trade.py` runs the pure-logic sanity checks (sizing + exit decisions) with no network or funds.
- `reference/demo_before_after.md` is the efficacy test: applied to a deliberately undisciplined bot, the skill flags seven distinct account-ending mistakes and produces the disciplined rewrite.

## License

MIT — ready to be merged or submoduled into the kit. See `LICENSE`.
