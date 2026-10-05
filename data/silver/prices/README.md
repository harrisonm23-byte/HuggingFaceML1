# Silver prices

`silver_daily_2011.csv`: daily silver price, USD per troy ounce, for 2011 (the year of 65 of the 94 chats, and of the replay's pilot day, 2011-01-07). Source: Financial Modeling Prep, symbol `SIUSD` (spot silver), end-of-day "light" series, pulled 2026-10-04 through the session's FMP connector.

- `close_usd_per_oz`: the vendor's end-of-day price. It is **not** the London silver fix (the noon auction at the centre of the case); the two are close on most days but not identical.
- `thin_day`: `yes` where volume is tiny (US/UK holidays, e.g. 2011-05-31, 2011-11-25). Treat those prices with care.
- Checks against known moves: the 2011-04-29 high near $48.60, the early-May crash (from about $48.60 down to about $35), and the 2011-09-22/23 drop from about $40.50 to about $30.

`xagusd_1min_bid_2011-01-07.csv`: 1-minute silver bars (XAG/USD, bid side, times in UTC) for the replay's pilot day, 2011-01-07, from Dukascopy's Historical Data Feed (downloaded by the user, 2026-10-04). 1,318 bars, 00:00-21:59 UTC (the market closes for the weekend at 22:00 UTC on Friday). Range $28.31-$29.32, consistent with the daily file (low $28.33, high $29.38; small differences are normal between vendors and bid vs. mid prices). Around the London fix (noon London = 12:00 UTC in January) silver traded near $28.40-$28.45. The jump after 13:30 UTC (from about $28.45 to about $29.15 by 15:00) lines up with the US jobs report released that morning.

`xagusd_1min_bid_2011-01-12.csv`, `xagusd_1min_bid_2011-04-01.csv`, `xagusd_1min_bid_2011-06-08.csv`, `xagusd_1min_bid_2011-08-05.csv`: 1-minute silver bars for the four later days of the multi-day replay. Same layout as the 2011-01-07 file: XAG/USD, bid side, times in UTC, columns `Etc/UTC,Open,High,Low,Close,Volume`, minutes with no trading left out. Source: Dukascopy's Historical Data Feed (`datafeed.dukascopy.com`, `BID_candles_min_1`), downloaded 2026-10-05. Check on the method: 2011-01-07 was downloaded and converted the same way and came out byte-for-byte identical to the file already here.

| File | Bars | First-last bar (UTC) | Low | High | Close in `silver_daily_2011.csv` |
|---|---|---|---|---|---|
| `xagusd_1min_bid_2011-01-12.csv` | 1,399 | 00:01-23:59 | 29.200 | 29.820 | 29.545 |
| `xagusd_1min_bid_2011-04-01.csv` | 1,260 | 00:00-20:59 | 37.053 | 37.834 | 37.732 |
| `xagusd_1min_bid_2011-06-08.csv` | 597 | 00:01-23:00 | 36.058 | 37.150 | 36.620 |
| `xagusd_1min_bid_2011-08-05.csv` | 1,260 | 00:00-20:59 | 37.512 | 39.813 | 38.211 |

Things to know before using these four days:

- **2011-06-08 is sparse.** Only 597 of the day's minutes have a bar; before 06:00 UTC there are 2-5 bars an hour. The feed is thin for this whole week (7 June has 516 bars, 9 June has 267), so it is the source, not a failed download. A minute without a bar means no recorded quote, not a flat price.
- **2011-01-12 has no bid/ask spread in the source.** Dukascopy's bid file and ask file for this day are identical, so these are effectively single-price bars rather than true bid prices. The other three days have a normal spread of about 4-5 cents.
- **Volume is not comparable across days.** On 7 Jan, 1 Apr and 5 Aug the source volume is fractional (typical bar 0.3-1.9, shown x1,000,000 as in the 7 Jan file). On 12 Jan and 8 Jun the source volume is whole numbers (typical bar 73 and 2), which look like quote counts; the same x1,000,000 is applied so the files stay consistent, but do not compare those numbers with the other days. Prices are unaffected.
- **Session ends differ.** 1 Apr and 5 Aug are Fridays in summer time, so the market closes at 21:00 UTC (7 Jan, a winter Friday, closes at 22:00 UTC). London noon is 12:00 UTC on 12 Jan and 11:00 UTC on the other three days.
- Ask-side files for the same days are available from the same feed.

Still to get: the other years (2007-2013; available from the same source), the London fix itself, and intraday prices for the days around the pilot day (Dukascopy, as above).
