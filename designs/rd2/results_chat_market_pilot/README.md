# Chat-and-trade pilot (Gemma 4 via the API), sessions kept in the repo

Each of 12 chats as a one-hour trading session on its real date (`sim/chat_market.py`, setups in
`data/silver/chat_market_pilot.json`), both conditions (takeover as the asked trader; extra party as Harbor Bank),
6 versions (real, 4 framed, no ask) x 3 runs. Stopped at 348 of 432 sessions on 2026-10-10 (the last three chats,
p277-p279, incomplete) when the work moved to the mountain. `sessions.jsonl`: every session with its steps (replies,
trades, positions, prices) and summary; the observation text is left out to keep the file small (the run folder
outputs/rd2_api/chat_market_pilot is not committed).

Known limits (the 2026-10-10 review; fixed in the mountain, not here): the price history paired each step's time with
the price 14 minutes later; the two 8 Jun chats opened on a price back-filled from a later minute; the disclosure
numbers are a keyword screen (it also counts refusals). The old parser misread no order in these sessions (checked
with the strict parser: 174 trades, 1,128 holds, 90 replies without TARGET/HOLD, 88 of them a QUOTE only).
