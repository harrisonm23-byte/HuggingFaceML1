# Silver prices

`silver_daily_2011.csv`: daily silver price, USD per troy ounce, for 2011 (the year of 65 of the 94 chats, and of the replay's pilot day, 2011-01-07). Source: Financial Modeling Prep, symbol `SIUSD` (spot silver), end-of-day "light" series, pulled 2026-10-04 through the session's FMP connector.

- `close_usd_per_oz`: the vendor's end-of-day price. It is **not** the London silver fix (the noon auction at the centre of the case); the two are close on most days but not identical.
- `thin_day`: `yes` where volume is tiny (US/UK holidays, e.g. 2011-05-31, 2011-11-25). Treat those prices with care.
- Checks against known moves: the 2011-04-29 high near $48.60, the early-May crash (from about $48.60 down to about $35), and the 2011-09-22/23 drop from about $40.50 to about $30.

Still to get: the other years (2007-2013; available from the same source), the London fix itself, and intraday prices for the replay (the intraday series needs a paid FMP plan, or another source).
