# Showcase: real questions, real answers

Nine unedited sessions from the live pipeline (September 2026). Two execution
profiles appear below: deep research (Claude Opus planner, 15–25 turns) and
fast tabular queries (glm-flash, 1–6 turns). Note the built-in **figure check**:
any number in the answer that does not appear in tool outputs is flagged for
the reader — the pipeline polices its own hallucinations.

---

## 1. Find potential arbitrageurs on OKX Wallet who are arbitraging shitcoins

*MCP / Claude Opus · 359 s · 22 turns · 18 tool calls (get_address_info, describe_table, query_evm_onchain, query_verified_tokens)*

**Bottom line.** Arbitrage of "shitcoins" via OKX Wallet right now lives **not as atomic on-chain arbitrage, but as DEX→CEX**: buying a low-liquidity token through the OKX DEX Router and depositing to an exchange within seconds/minutes. The main chain is **Robinhood Chain** (484,647 swaps / 38,792 wallets over 7 days through OKX routers; on X Layer — only 348 swaps).

Atomic arb (a "token → … → same token" cycle within a single tx) through the OKX router: **1 transaction over 7 days** — it essentially doesn't exist; MEV bots don't use the aggregator.

**Arbitrageur candidates (7 days):**

| Wallet | Swaps (via OKX router) | Tokens | CEX deposits | Median "buy → deposit" |
|---|---|---|---|---|
| `0x26c2448c…` | 15,646 (24) | 7 | 333 → OKX | **9 sec** (p25 = 4 s) |
| `0xb80d90fc…` | 2,956 (198) | 44 | 130 Gate / 79 OKX / 50 KuCoin | p25 = **9 sec** |
| `0x88538812…` | 2,770 (all via OKX) | 44 | 19 → LBank | p25 = 626 s |
| `0x2c102447…` | 772 (all via OKX) | 6 | 15 → Gate | p25 = 154 s |
| `0x38dface8…` | 394 (392) | 25 | 21 → OKX | **125 sec** (p25 = 45 s) |

The cleanest profile is `0xb80d90fc…`: a closed cycle Gate → on-chain purchase → deposit to Gate/OKX/KuCoin, 44 tokens, three exchanges. Plus a list of fast "flippers" with no CEX connection (213 tokens / 186 s median hold, etc.).

*Limitations stated in the answer: PnL not computed (no USD prices for these tokens) — pattern only; exchange attribution from deposit-address labels.*

---

## 2. Which tokens on OKX have the highest OI and volume with potentially manipulative pumping?

*MCP / Claude Opus · 363 s · 17 turns · 15 tool calls (query_cex_normalized, query_cex_aggregates, get_and_calc_cex_technical_analysis)*

Leaders table (OI, ΔOI, volume, Δprice, taker skew) for BTC/ETH/SOL/ZEC/XRP/NEAR/LINK/ONDO/SUI/XPL, then:

**Potentially manipulative pump (high risk):**
1. **XPL** — volume 7.2x ($35M→$256M), price +15%, but OI only $9.7M: turnover 26× open interest; OI even fell over 4h. Classic churn profile.
2. **ONDO** — volume 1.95x, price +9%, but taker skew −3.2% (net selling) and OI −10.4% over 4h. Distribution into strength.
3. **ZEC** — most concentrated OI ($187M), last-hour OI cut −4.7%, price at resistance with 4h RSI 44.7 (bearish divergence).
4. **SPCX** — OI +15.2% with price exactly flat and falling volume — setup for a squeeze.

**More like continuation:** SOL (shorts liquidated $2.78M vs longs $1.04M, early positioning), LINK (breakout confirmed by volume), SUI, XRP. Long-squeeze risk: NEAR.

---

## 3. Who on X Layer got into fresh tokens earliest this week: 5 wallets, entries, average buy size

*MCP / Claude Opus · 422 s · 21 turns · 18 tool calls*

Top-5 table (21–18 entries into top-10 first buyers, average buy $137–148), and then the part that makes this pipeline different — it **called out its own finding**:

> **Important caveat: this is not "alpha hunters" but a single bot cluster.** All five enter the same tokens, exactly 2 purchases per token, 20–60 seconds apart; tokens appear on a ~47-minute schedule; uniform $125–155 tickets — a farming/market-making signature on a launchpad.

Re-ranked strictly by top-3 first buyers, it isolated the one profile resembling deliberate sniping (`0x36c1798c…`: 2× ticket, first buyer 5 times). Methodology block included (494 fresh tokens in window, 110 with ≥20 buyers, OKB priced at $119.5–120.0).

---

## 4. OKX liquidations over the past week by day: which coins wipe longs vs shorts, in dollars

*MCP / Claude Opus · 195 s · 8 turns · 6 tool calls*

**Total for the week: $371.8M** — longs $170.5M, shorts $201.2M. Per-day table (worst day 09.18: $53.8M shorts squeezed; main long wipeout 09.23: $45.8M / 12,390 events). "Most often wipe longs": SKHYNIX 82%, SPCX 80%, WLD 68%, TRUMP 62%… "Most often wipe shorts": USELESS 77%, LTC 65%, SOL 63%, BTC 62%…

**Conclusion:** the week went against shorts on majors (BTC/ETH/SOL/SUI ≈62% short liqs); longs took the hit in tokenized stocks / AI narratives (SKHYNIX, SPCX, WLD, ONDO, TRUMP). Caveats: linear USDT perps only; last day incomplete.

---

## 5. How much volume passed on OKX in 24h for BTC, ETH and SOL? As a table

*PIPELINE / glm-flash · 1 tool call*

$ETH $6.82B, $BTC $6.33B, $SOL $1.58B — total $14.73B (linear USDT swaps; sum of hourly volume × close; 24/24 bars coverage stated).

*Figure check flagged: derived totals (`14.73`) marked as model-computed — double-check.*

---

## 6. Top 10 coins on OKX by 24h volume with price change, in a table

*PIPELINE / glm-flash · 1 tool call*

Full top-10 table ($ETH $6.75B +0.18% … $XPL $248M +3.43%), with observations: top-2 hold 84% of top-10 volume; gainers led by SUI +13.16%, NEAR +9.13%, ONDO +6.97% — rotation from flat majors into volatile tail.

*Figure check flagged: `84%`, `77%` are derived — double-check.*

---

## 7. Top-10 coins on OKX by 24h open-interest growth: current OI, growth %, price change

*PIPELINE / glm-flash · 6 turns (one query error self-recovered)*

Table led by $TMF +67.73% OI with −1.16% price (short accumulation signal); healthy long expansion on $CC/$AERO/$GRASS (OI +35–43% with price +13.75–20.84%).

*Figure check flagged several derived aggregates.*

---

## 8. Which coins on OKX collected the most long and short liquidations in 24h? Table with $ amounts

*PIPELINE / glm-flash · 1 tool call*

Top-10 table ($ETH $8.29M total, $BTC $4.51M, $ZEC $3.17M, tokenized-stock $SNDK $2.81M…), directional read (shorts squeezed on ETH/ORDI; longs hit on BTC/SNDK), market-wide stats (100 coins, avg liquidation $39K).

*Figure check flagged derived shares.*

---

## 9. Compare X Layer vs Robinhood Chain activity over 24h: swaps, wallets, $ volume, top-3 tokens

*MCP / Claude Opus · 641 s · 25 turns · 19 tool calls (incl. live multicall to both chains for symbols)*

| Metric | Robinhood Chain | X Layer | Gap |
|---|---|---|---|
| Swaps | 2,325,721 | 132,188 | 17.6× |
| Unique wallets | 256,653 | 16,080 | 16× |
| $ volume (stable leg) | $336.3M | $23.9M | 14× |

Top-3 on X Layer = **tokenized stocks**: AAPLx $8.08M, TSLAx $2.75M, NVDAx $2.61M (56% of measured volume). Conclusion drawn with explicit caveats: stable-leg volume is a lower bound; native-leg pricing on RH rejected after the pipeline noticed inconsistent amounts rather than publishing a garbage number.

---

### What these sessions demonstrate

- **Facts, not vibes**: every claim traces to tool calls over indexed data; derived numbers are flagged by the figure check.
- **Self-skepticism**: example 3 demoted its own headline finding to "bot cluster" instead of selling it as alpha; example 9 refused a garbage price estimate.
- **Depth on demand**: the same API served 1-call table lookups and 25-turn investigations — governed by `max_cost_usd`.
