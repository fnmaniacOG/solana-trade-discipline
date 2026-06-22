"""
risk_managed_trade.py — reference implementation for the solana-trade-discipline skill.

A full risk-managed trade lifecycle:  size -> enter -> set stop/target -> manage exit.

This is a TEMPLATE. The `kit_*` functions are placeholders for the Solana AI Kit's
existing primitives (Jupiter swap, Pyth/DexPaprika price). Wire them to the real
ones; the discipline logic around them is the point. Pure functions (sizing, exit
decisions) are written so they can be unit-tested with NO network and NO funds —
build and verify the brain offline, then connect the hands on devnet.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


# --------------------------------------------------------------------------- #
# Pure logic — testable offline, no network, no keys, no funds.
# --------------------------------------------------------------------------- #
def size_from_risk(account_equity: float, risk_pct: float,
                   entry: float, stop: float) -> float:
    """Tokens to buy so that being stopped out loses exactly risk_pct of equity.
    A wider stop -> smaller size. Risk stays constant. (See sizing.md)"""
    risk_dollars = account_equity * (risk_pct / 100.0)
    per_unit = abs(entry - stop)
    if per_unit <= 0:
        raise ValueError("stop must differ from entry")
    return risk_dollars / per_unit


def net_rr(entry: float, stop: float, target: float, cost_per_unit: float) -> float:
    """Reward:risk AFTER round-trip costs. Below 2.0 -> skip the trade. (sizing.md)"""
    risk = abs(entry - stop) + cost_per_unit
    reward = abs(target - entry) - cost_per_unit
    return round(reward / risk, 2) if risk > 0 and reward > 0 else 0.0


@dataclass
class Position:
    symbol: str
    direction: str            # "LONG" | "SHORT"
    entry: float
    size: float               # tokens
    stop: float
    target1: float
    target2: float
    opened_at: datetime
    max_hold_hours: float = 72.0
    half_taken: bool = False
    stop_at_breakeven: bool = False
    realized: float = 0.0


def decide(pos: Position, price: float, now: datetime) -> dict:
    """The mechanical exit decision. Returns one action — never improvised. (exits.md)
    actions: HOLD | TRIM_T1 | EXIT_STOP | EXIT_T2 | EXIT_TIME"""
    long = pos.direction == "LONG"
    stop = pos.entry if pos.stop_at_breakeven else pos.stop
    hit_stop = price <= stop if long else price >= stop
    hit = lambda lvl: (price >= lvl) if long else (price <= lvl)

    if hit_stop:
        return {"action": "EXIT_STOP", "fraction": 1.0, "price": stop}
    if hit(pos.target2):
        return {"action": "EXIT_T2", "fraction": 1.0, "price": pos.target2}
    if not pos.half_taken and hit(pos.target1):
        # scale half, then stop goes to breakeven — the rest is risk-free
        return {"action": "TRIM_T1", "fraction": 0.5, "price": pos.target1}
    age_h = (now - pos.opened_at).total_seconds() / 3600.0
    if age_h >= pos.max_hold_hours:
        return {"action": "EXIT_TIME", "fraction": 1.0, "price": price}
    return {"action": "HOLD", "fraction": 0.0, "price": price}


# --------------------------------------------------------------------------- #
# Execution layer — placeholders for the kit's real primitives.
# Replace with Jupiter swap / Pyth price / etc. Test on devnet first.
# --------------------------------------------------------------------------- #
def kit_get_price(symbol: str) -> float:        # -> Pyth / DexPaprika
    raise NotImplementedError("wire to the kit's price primitive")

def kit_swap(symbol: str, side: str, size: float, max_slippage_bps: int) -> dict:
    # -> Jupiter swap, with an EXPLICIT slippage cap and confirmation. (execution.md)
    raise NotImplementedError("wire to the kit's swap primitive; confirm before updating state")


# --------------------------------------------------------------------------- #
# Lifecycle — the disciplined path. Entry only fires if the plan checks out.
# --------------------------------------------------------------------------- #
def open_trade(symbol, direction, account_equity, risk_pct, entry, stop,
               target1, target2, cost_per_unit, max_slippage_bps=50) -> Position | None:
    rr = net_rr(entry, stop, target1, cost_per_unit)
    if rr < 2.0:
        print(f"SKIP {symbol}: net R:R {rr} < 2.0 after costs — no edge.")
        return None
    size = size_from_risk(account_equity, risk_pct, entry, stop)
    fill = kit_swap(symbol, "buy" if direction == "LONG" else "sell", size, max_slippage_bps)
    # use the REAL filled price/size, not the intended ones
    real_entry, real_size = fill["avg_price"], fill["filled_size"]
    return Position(symbol, direction, real_entry, real_size,
                    stop, target1, target2, datetime.now(timezone.utc))


def manage(pos: Position) -> Position | None:
    """Poll and act on the rule. Returns the (possibly updated) position, or None if closed."""
    price = kit_get_price(pos.symbol)
    instr = decide(pos, price, datetime.now(timezone.utc))
    if instr["action"] == "HOLD":
        return pos
    qty = pos.size * instr["fraction"]
    kit_swap(pos.symbol, "sell" if pos.direction == "LONG" else "buy", qty, max_slippage_bps=50)
    if instr["action"] == "TRIM_T1":
        pos.size -= qty
        pos.half_taken = True
        pos.stop_at_breakeven = True       # <- the move that makes the rest risk-free
        return pos
    return None  # fully closed (stop / T2 / time)


if __name__ == "__main__":
    # offline sanity check of the pure logic — no network/funds needed
    p = Position("DEMO", "LONG", entry=100, size=10, stop=95,
                 target1=110, target2=120, opened_at=datetime.now(timezone.utc))
    assert decide(p, 94, datetime.now(timezone.utc))["action"] == "EXIT_STOP"
    assert decide(p, 111, datetime.now(timezone.utc))["action"] == "TRIM_T1"
    assert size_from_risk(1000, 1.0, 100, 95) == 2.0   # risk $10 / $5 per unit = 2 tokens
    print("pure logic checks pass")
