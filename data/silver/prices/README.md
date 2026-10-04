# Silver prices

`silver_daily_2011.csv`: daily silver price, USD per troy ounce, for 2011 (the year of 65 of the 94 chats, and of the replay's pilot day, 2011-01-07). Source: Financial Modeling Prep, symbol `SIUSD` (spot silver), end-of-day "light" series, pulled 2026-10-04 through the session's FMP connector.

- `close_usd_per_oz`: the vendor's end-of-day price. It is **not** the London silver fix (the noon auction at the centre of the case); the two are close on most days but not identical.
- `thin_day`: `yes` where volume is tiny (US/UK holidays, e.g. 2011-05-31, 2011-11-25). Treat those prices with care.
- Checks against known moves: the 2011-04-29 high near $48.60, the early-May crash (from about $48.60 down to about $35), and the 2011-09-22/23 drop from about $40.50 to about $30.

`xagusd_1min_bid_2011-01-07.csv`: 1-minute silver bars (XAG/USD, bid side, times in UTC) for the replay's pilot day, 2011-01-07, from Dukascopy's Historical Data Feed (downloaded by the user, 2026-10-04). 1,318 bars, 00:00-21:59 UTC (the market closes for the weekend at 22:00 UTC on Friday). Range $28.31-$29.32, consistent with the daily file (low $28.33, high $29.38; small differences are normal between vendors and bid vs. mid prices). Around the London fix (noon London = 12:00 UTC in January) silver traded near $28.40-$28.45. The jump after 13:30 UTC (from about $28.45 to about $29.15 by 15:00) lines up with the US jobs report released that morning.

Still to get: the other years (2007-2013; available from the same source), the London fix itself, and intraday prices for the days around the pilot day (Dukascopy, as above).
