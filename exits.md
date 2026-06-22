# Exits & Trade Management

Exits are where strategies live or die. A great entry with sloppy exits loses; a mediocre entry with disciplined exits survives. The single most common way retail traders bleed out is **small wins, big losses** — cutting winners early out of fear and letting losers run out of hope. Everything here exists to invert that.

## The one rule that prevents the most damage

**Define the full exit before you enter, and enforce it with a resting order — not your attention.**

A stop you "intend to watch for" is not a stop; it's a hope. Place the stop and target as actual orders the moment the entry fills. The order executes the plan when you're calm; your live nervous system, mid-trade, will not. If the venue can't hold a resting stop, the bot must poll and fire it automatically — the decision is never deferred to a human in the moment.

## Stops

- The stop marks **invalidation** — the price at which your thesis is wrong — not an arbitrary percentage. Place it where the reason for the trade no longer holds.
- **Never widen a stop.** Moving it further away to avoid being wrong is the account-ending habit. A stop only ever moves *toward* profit.
- Size the position *from* the stop distance (see `sizing.md`): risk a fixed % of the account between entry and stop. A wider stop means a smaller position, not more risk.
- A daily/structural close beyond the stop is final — don't "give it room" past invalidation.

## Targets, scale-outs, and the breakeven move

The standard disciplined pattern:

1. **Scale a portion off at T1** (e.g., half). This banks profit and de-risks.
2. **Move the stop to breakeven** on the remainder the moment T1 fills. Now the trade cannot become a loss — it's a free roll.
3. **Trail the rest toward T2** (and beyond), letting the winner run while the trailing stop protects gains.

This structure is what actually lets winners run *without* giving back the whole move: you've already banked some, the rest is risk-free, and the trail captures the trend.

## Trailing stops

- Trail only after the trade is in profit (typically after T1 / breakeven).
- Trail by a volatility measure (e.g., a multiple of ATR) or a structural level — not a fixed tick — so normal noise doesn't shake you out.
- The trail only ratchets one direction. It never loosens.

## Time stops

A trade that hasn't worked in the window you allotted is a "no." Capital sitting in a thesis that isn't playing out is capital not working elsewhere — and for options/perps it bleeds (theta/funding). Set a max-hold and exit when it's hit, regardless of price.

## The diagnostic that tells you if your exits are healthy

Track, across closed trades:

- **Win rate** (% of trades that profit)
- **Average win vs average loss** → the **payoff ratio**
- **Expectancy** = (win% × avg win) − (loss% × avg loss)
- **Plan-adherence %** = fraction of exits taken by the rule vs overridden manually

The trap to watch for: you can win 60% of trades and still lose money if your average loss is bigger than your average win. If `avg loss > avg win`, the exits are broken — winners are being cut and losers held. Drive the payoff ratio above 1 and adherence above ~80%, and the equity curve fixes itself. **The number to be proud of is adherence, not win rate.**

## Anti-patterns (the things that quietly kill accounts)

- Widening a stop "just this once."
- Buying *more* of a loser to lower the average (averaging down without a plan).
- Taking profit early because it "feels" like enough, with no rule behind it.
- Chasing a position after a move has already happened (buying the spike).
- Managing the exit by feel because you're watching it live. Pre-commit, then look away.

## Hard-won rules (paid for in real losses)

These aren't theory. The most expensive lesson behind this file: **$10K+ of borrowed money lost in a few weeks** on illiquid NFTs by breaking nearly every rule below — no stop, no plan, adding to a loser, hoping instead of cutting. The rules exist so an agent never repeats it.

- **CLQ — Cut Losses Quickly.** The first and most important. A small loss taken on plan is the cost of doing business; a large loss held in hope is how accounts die.
- **Never add to a loser.** Averaging down without a pre-planned scale-in is throwing good money after a broken thesis. Only add if adding was *part of the plan before entry.*
- **Take singles.** Bank partial profits in pieces; don't swing every trade for a home run. Consistent singles beat rare grand slams.
- **Let winners run** — but only the risk-free remainder, after you've banked a piece and moved the stop to breakeven. That's how "let it run" doesn't become "gave it all back."
- **Taking profits too soon makes your wins smaller than your losses.** Cutting winners early is the mirror image of holding losers — same fatal asymmetry. The scale-out + trail structure fixes it.
- **You can always get back in.** The fear that drives chasing and early exits is "I'll miss it." You won't — a re-entry on plan is always available. Missing a trade costs nothing; a bad fill costs money.
- **Don't chase.** If price has already run past your entry, the trade is gone. Wait for the next setup; don't buy the spike.
- **No profit is guaranteed** until it's realized. An unrealized gain is a loan the market can call back.
