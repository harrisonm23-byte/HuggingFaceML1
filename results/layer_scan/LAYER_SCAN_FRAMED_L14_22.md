# The layer scan with framed requests (exploratory)

16 moments (B's 10 neutral careers at the 7 and 12 January requests; 4 more left out because the scored orders cover less than half of the model's probability with the neutral request). UBS's request in each of its five framings; each document type's after-reading state (minus the neutral document's) added at layer 14 or 22 at 2 times its size. P(the order goes along) after the fixed neutral reasoning line. Produced by `designs/rd2/analysis/layer_scan_framed.py`.

## No injection: the framing's own effect

| Request | P(along) | Against the neutral request |
|---|---|---|
| neutral | 36.1% | – |
| loss | 52.4% | +16.4 (p 0.008) |
| gain | 44.2% | +8.2 (p 0.009) |
| loss + you | 47.6% | +11.6 (p 0.007) |
| gain + you | 49.9% | +13.8 (p 0.009) |

## Layer 14: each state's change from no injection, under each framing (points)

| Request | loss | blame | gain | credit | random |
|---|---|---|---|---|---|
| neutral | +21.0 (p 0.007) | +21.7 (p 0.015) | +22.0 (p 0.008) | +23.1 (p 0.008) | +0.1 (p 0.984) |
| loss | +8.1 (p 0.008) | +9.2 (p 0.014) | +10.6 (p 0.008) | +11.3 (p 0.007) | -11.8 (p 0.245) |
| gain | +15.3 (p 0.014) | +17.1 (p 0.031) | +17.6 (p 0.020) | +18.4 (p 0.032) | -8.9 (p 0.370) |
| loss + you | +6.7 (p 0.015) | +8.2 (p 0.028) | +8.6 (p 0.014) | +9.3 (p 0.024) | -5.0 (p 0.640) |
| gain + you | +9.5 (p 0.018) | +10.1 (p 0.008) | +10.0 (p 0.024) | +10.4 (p 0.023) | -12.3 (p 0.191) |

Against random at layer 14: neutral: loss +20.9 (p 0.072), blame +21.6 (p 0.037), gain +21.9 (p 0.040), credit +23.1 (p 0.039); loss: loss +19.8 (p 0.007), blame +20.9 (p 0.009), gain +22.4 (p 0.007), credit +23.1 (p 0.010); gain: loss +24.2 (p 0.009), blame +26.1 (p 0.009), gain +26.5 (p 0.009), credit +27.3 (p 0.008); loss + you: loss +11.7 (p 0.259), blame +13.2 (p 0.190), gain +13.6 (p 0.137), credit +14.3 (p 0.054); gain + you: loss +21.8 (p 0.008), blame +22.4 (p 0.008), gain +22.2 (p 0.007), credit +22.7 (p 0.007).

## Layer 22: each state's change from no injection, under each framing (points)

| Request | loss | blame | gain | credit | random |
|---|---|---|---|---|---|
| neutral | +22.1 (p 0.040) | +24.0 (p 0.037) | +28.0 (p 0.007) | +23.2 (p 0.009) | +15.4 (p 0.098) |
| loss | +7.7 (p 0.449) | +8.6 (p 0.286) | +16.3 (p 0.009) | +12.4 (p 0.010) | +0.0 (p 0.993) |
| gain | +15.0 (p 0.040) | +16.0 (p 0.047) | +21.9 (p 0.009) | +16.8 (p 0.031) | +8.3 (p 0.238) |
| loss + you | +11.8 (p 0.007) | +15.2 (p 0.016) | +20.9 (p 0.007) | +14.6 (p 0.009) | +3.9 (p 0.682) |
| gain + you | +8.9 (p 0.007) | +11.3 (p 0.008) | +18.5 (p 0.008) | +13.0 (p 0.009) | +1.6 (p 0.939) |

Against random at layer 22: neutral: loss +6.7 (p 0.015), blame +8.6 (p 0.023), gain +12.6 (p 0.008), credit +7.8 (p 0.280); loss: loss +7.7 (p 0.009), blame +8.6 (p 0.008), gain +16.3 (p 0.008), credit +12.4 (p 0.009); gain: loss +6.7 (p 0.017), blame +7.7 (p 0.008), gain +13.6 (p 0.007), credit +8.6 (p 0.068); loss + you: loss +7.9 (p 0.008), blame +11.3 (p 0.005), gain +17.0 (p 0.007), credit +10.7 (p 0.131); gain + you: loss +7.3 (p 0.011), blame +9.7 (p 0.006), gain +16.9 (p 0.007), credit +11.4 (p 0.007).

## The agent's own replies (two sampled per moment): share that went along

| Request | none | blame x2 at layer 14 | blame x2 at layer 22 | loss x2 at layer 14 | loss x2 at layer 22 |
|---|---|---|---|---|---|
| neutral | 19% (32) | 28% (32) | 56% (32) | 28% (32) | 50% (32) |
| loss | 44% (32) | 34% (32) | 62% (32) | 44% (32) | 59% (32) |
| gain | 19% (32) | 19% (32) | 59% (32) | 38% (32) | 50% (32) |
| loss + you | 31% (32) | 44% (32) | 56% (32) | 41% (32) | 62% (32) |
| gain + you | 38% (32) | 53% (32) | 53% (32) | 44% (32) | 53% (32) |

Unreadable replies overall: 7%.
