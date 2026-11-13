"""The financial document set (designs/rd2/financial_docs/; the user, 22 Oct): summaries of real, cited financial
reports, one document per paragraph, in three matched types (13 each, about 130 words; sources in SOURCE_REGISTER.csv).
Frozen: the files are checked against these fingerprints before use."""
import hashlib, os

LISTS = "designs/rd2/financial_docs"
THEMES = ["neutral", "loss", "gain"]
FROZEN = {"neutral": "fabf45720dcf58f874b835c2fcd9c070ef04225b58aa3e0a26c768eaac4eadd0",
          "loss": "262acd301f7efac8726f14a03cfd0008e2d4aa46a8414cf6f126524acef6440e",
          "gain": "4bd4deb3119610700716f5a729948db8814cc93d4631dc5207db1e4b5bbd1a18"}


def read_docs(root="."):
    """{theme: [documents]}, from the frozen files (refuses a file that has changed)."""
    out = {}
    for t, sha in FROZEN.items():
        path = os.path.join(root, LISTS, f"{t}.txt")
        assert hashlib.sha256(open(path, "rb").read()).hexdigest() == sha, f"{path} changed since it was frozen"
        out[t] = [d.strip() for d in open(path, encoding="utf-8") if d.strip()]
    return out
