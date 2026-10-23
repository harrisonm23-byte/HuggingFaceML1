# Financial valence state-injection corpus — pilot v6

## Files to feed into Gemma

- `GEMMA_LOSS.txt`
- `GEMMA_GAIN.txt`
- `GEMMA_NEUTRAL.txt`

Each stimulus is a **continuous concatenation** of thirteen financially themed passages, with no condition headers, dates, metadata, source names, or URLs added beyond names naturally occurring in the prose. Passages are separated by blank lines. Condition names appear only in filenames.

## What the text is

The initial phrase of each passage is a short, authentic excerpt (generally a headline fragment or release sentence). The remaining paragraphs are **newly written, source-based condensed adaptations**, NOT verbatim article extracts. Original source URLs appear in `SOURCE_REGISTER.csv` and `*_ANNOTATED.md`. This distinction is important: do not call the complete files verbatim source documents. The complete source articles remain accessible through those URLs.

The neutral passages are descriptions of business operations and market mechanisms, not actual press reports of neutral earnings. They deliberately avoid reported profits and price changes.

The corpus excludes tech-company earnings. It begins with Deutsche Bank, then other major banks, then silver/gold/oil, then equity-market moves. Dates are retained in the source register but omitted from model-facing text where practical. The LOSS passages deliberately avoid litigation references. Corporate source pages may themselves discuss litigation elsewhere; only the passages included here were screened.

## Important experimental cautions

- Equal numbers of passages do not guarantee matched tokens. See counts below.
- A mid-document intervention requires comparing identical target layers/positions; an unequal prefill can itself change activation distributions. If exact token matching matters, truncate or build per-passage batches with the tokenizer used for Gemma.
- The April 2011 silver rally and September 2011 silver crash could convey post-event market information to a historically simulated 2011 trader. For a pure state injection study, record this as a limitation and omit those items if the model might use dates and prices as trading information.
- The neutral documents are functionally neutral but topic matched; they are not journalism-style news releases.
- Silver futures **volume** records do not imply that silver prices or long positions gained; this source is explicitly classified as market-activity growth.
- Corporate press releases and news articles may be protected by copyright; only brief quotations are reproduced here. Read the original source at the recorded URL for full prose.

## Rough corpus size

- LOSS: 13 passages; 2,366 words; approximately 4,156 character-estimated tokens.
- GAIN: 13 passages; 2,175 words; approximately 3,760 character-estimated tokens.
- NEUTRAL: 13 passages; 1,835 words; approximately 3,505 character-estimated tokens.

Actual model token counts depend on the Gemma tokenizer.

## Lightly length-matched alternative

Use `GEMMA_LOSS_MATCHED.txt`, `GEMMA_GAIN_MATCHED.txt`, and `GEMMA_NEUTRAL_MATCHED.txt` to get closer to equal word count. For LOSS and GAIN, short excerpts and complete sentences were retained; explanatory trailing sentences were removed to make length comparable. The NEUTRAL material is used at full length. These are **approximate word** counts, not verified Gemma token counts. The original longer texts remain in `GEMMA_*.txt`.

- LOSS matched: 1,843 words.
- GAIN matched: 1,873 words.
- NEUTRAL matched: 1,825 words.

## Lightly length-matched alternative

Use `GEMMA_LOSS_MATCHED.txt`, `GEMMA_GAIN_MATCHED.txt`, and `GEMMA_NEUTRAL_MATCHED.txt` to get closer to equal word count. For LOSS and GAIN, short excerpts and complete sentences were retained; explanatory trailing sentences were removed to make length comparable. The NEUTRAL material is used at full length. These are **approximate word** counts, not verified Gemma token counts. The original longer texts remain in `GEMMA_*.txt`.

- LOSS matched: 1,843 words.
- GAIN matched: 1,870 words.
- NEUTRAL matched: 1,825 words.

## Counts in the full versions (recomputed)

- LOSS full: 2,362 words.
- GAIN full: 2,144 words.
- NEUTRAL full: 1,825 words.
