# The layer scan with framed requests (exploratory)

16 moments (B's 10 neutral careers at the 7 and 12 January requests; 4 more left out because the scored orders cover less than half of the model's probability with the neutral request). UBS's request in each of its five framings; each document type's after-reading state (minus the neutral document's) added at layer 19 or 21 at 2 times its size. P(the order goes along) after the fixed neutral reasoning line. Produced by `designs/rd2/analysis/layer_scan_framed.py`.

## No injection: the framing's own effect

| Request | P(along) | Against the neutral request |
|---|---|---|
| neutral | 36.1% | – |
| loss | 52.4% | +16.4 (p 0.008) |
| gain | 44.2% | +8.2 (p 0.009) |
| loss + you | 50.8% | +11.6 (p 0.007) |
| gain + you | 53.1% | +13.8 (p 0.009) |

## Layer 19: each state's change from no injection, under each framing (points)

| Request | loss | blame | gain | credit | random |
|---|---|---|---|---|---|
| neutral | +17.3 (p 0.007) | +27.0 (p 0.016) | +2.7 (p 0.412) | +4.9 (p 0.295) | +2.7 (p 0.742) |
| loss | +14.2 (p 0.008) | +19.1 (p 0.007) | -1.7 (p 0.598) | -0.3 (p 0.951) | -6.9 (p 0.015) |
| gain | +13.9 (p 0.007) | +25.1 (p 0.015) | -1.5 (p 0.779) | -0.1 (p 0.934) | -4.0 (p 0.382) |
| loss + you | +10.4 (p 0.007) | +17.3 (p 0.014) | -1.6 (p 0.977) | +0.8 (p 0.634) | -2.3 (p 0.528) |
| gain + you | +10.0 (p 0.024) | +18.0 (p 0.027) | -1.3 (p 0.359) | +1.6 (p 0.501) | -4.3 (p 0.088) |

Against random at layer 19: neutral: loss +14.6 (p 0.071), blame +24.3 (p 0.016), gain -0.0 (p 0.985), credit +2.2 (p 0.824); loss: loss +21.1 (p 0.007), blame +26.0 (p 0.009), gain +5.1 (p 0.007), credit +6.6 (p 0.010); gain: loss +17.5 (p 0.009), blame +29.1 (p 0.009), gain +2.6 (p 0.684), credit +3.9 (p 0.264); loss + you: loss +12.7 (p 0.009), blame +19.6 (p 0.007), gain +0.6 (p 0.763), credit +3.1 (p 0.639); gain + you: loss +14.2 (p 0.008), blame +22.2 (p 0.008), gain +3.0 (p 0.418), credit +5.9 (p 0.126).

## Layer 21: each state's change from no injection, under each framing (points)

| Request | loss | blame | gain | credit | random |
|---|---|---|---|---|---|
| neutral | +24.2 (p 0.010) | +26.0 (p 0.028) | +8.1 (p 0.146) | -0.7 (p 0.897) | +16.0 (p 0.110) |
| loss | +12.5 (p 0.078) | +12.8 (p 0.097) | -0.1 (p 1.000) | -7.7 (p 0.248) | +5.2 (p 0.155) |
| gain | +14.7 (p 0.086) | +17.5 (p 0.126) | +2.5 (p 0.632) | -3.9 (p 0.829) | +11.9 (p 0.173) |
| loss + you | +11.9 (p 0.007) | +13.2 (p 0.144) | +4.2 (p 0.526) | -4.1 (p 0.552) | +6.5 (p 0.432) |
| gain + you | +10.1 (p 0.139) | +11.2 (p 0.138) | +5.4 (p 0.574) | -0.6 (p 0.753) | +3.5 (p 0.813) |

Against random at layer 21: neutral: loss +8.1 (p 0.007), blame +9.9 (p 0.008), gain -7.9 (p 0.109), credit -16.8 (p 0.024); loss: loss +7.3 (p 0.255), blame +7.6 (p 0.071), gain -5.3 (p 0.441), credit -12.9 (p 0.100); gain: loss +2.9 (p 0.626), blame +5.6 (p 0.133), gain -9.4 (p 0.362), credit -15.8 (p 0.055); loss + you: loss +5.4 (p 0.008), blame +6.6 (p 0.005), gain -2.3 (p 0.490), credit -10.6 (p 0.034); gain + you: loss +6.6 (p 0.011), blame +7.7 (p 0.006), gain +1.9 (p 0.141), credit -4.1 (p 0.187).

## The agent's own replies (two sampled per moment): share that went along

| Request | none | blame x2 at layer 19 | blame x2 at layer 21 | loss x2 at layer 19 | loss x2 at layer 21 |
|---|---|---|---|---|---|
| neutral | 38% (32) | 22% (32) | 50% (32) | 12% (32) | 47% (32) |
| loss | 50% (32) | 28% (32) | 59% (32) | 34% (32) | 59% (32) |
| gain | 22% (32) | 20% (30) | 63% (30) | 34% (32) | 47% (30) |
| loss + you | 40% (30) | 30% (30) | 47% (30) | 30% (30) | 60% (30) |
| gain + you | 37% (30) | 30% (30) | 53% (30) | 23% (30) | 50% (30) |

Unreadable replies overall: 5%.
