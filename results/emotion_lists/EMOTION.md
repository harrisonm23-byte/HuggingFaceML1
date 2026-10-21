# The author's emotion lists against the frame UBS's lines produce (exploratory)

Documents: blame 16, credit 16, gain 16, loss 16. Each read on its own by Gemma 3 12B (bfloat16); its state is the mean over its tokens. UBS's directions come from the matched rereads (the history held fixed). Cosine: 1 = the same direction, 0 = unrelated (two random directions in this space: about +/-0.03). The null reshuffles which documents belong to which theme. Produced by `designs/rd2/analysis/emotion_lists.py`.


## Loss - Gain, against UBS: loss - gain request

| Layer | Cosine | Null, 95% range | Cosine, dimensions on one scale | Null, 95% range | Emotion direction, two halves of the documents | UBS direction, two halves of the careers | Held out: documents sorted right |
|---|---|---|---|---|---|---|---|
| 6 | +0.211 | -0.385 to +0.378 | +0.028 | -0.042 to +0.043 | +0.977 | +0.998 | 100% |
| 12 | +0.257 | -0.288 to +0.290 | +0.097 | -0.097 to +0.098 | +0.974 | +0.916 | 100% |
| 18 | -0.281 | -0.533 to +0.534 | +0.079 | -0.083 to +0.081 | +0.977 | +0.997 | 94% |
| 24 | +0.097 | -0.092 to +0.090 | +0.076 | -0.079 to +0.076 | +0.809 | +0.984 | 94% |
| 31 | +0.076 | -0.194 to +0.204 | +0.098 | -0.102 to +0.104 | +0.911 | +0.962 | 100% |
| 36 | +0.344 | -0.486 to +0.479 | +0.101 | -0.106 to +0.107 | +0.965 | +0.967 | 100% |
| 41 | +0.395 | -0.488 to +0.485 | +0.106 | -0.109 to +0.108 | +0.983 | +0.953 | 100% |
| 47 | +0.181 | -0.403 to +0.393 | +0.099 | -0.106 to +0.107 | +0.982 | +0.888 | 100% |

## Blame - Loss (the "you" in a loss), against UBS: loss + you - loss

| Layer | Cosine | Null, 95% range | Cosine, dimensions on one scale | Null, 95% range | Emotion direction, two halves of the documents | UBS direction, two halves of the careers | Held out: documents sorted right |
|---|---|---|---|---|---|---|---|
| 6 | +0.074 | -0.180 to +0.167 | +0.060 | -0.061 to +0.060 | +0.966 | +0.991 | 100% |
| 12 | -0.019 | -0.508 to +0.531 | +0.051 | -0.057 to +0.057 | +0.966 | +0.987 | 100% |
| 18 | -0.844 | -0.943 to +0.946 | +0.028 | -0.037 to +0.038 | +0.868 | +1.000 | 84% |
| 24 | -0.452 | -0.769 to +0.767 | +0.009 | -0.038 to +0.036 | +0.743 | +0.998 | 84% |
| 31 | -0.093 | -0.660 to +0.660 | +0.025 | -0.044 to +0.044 | +0.953 | +0.994 | 100% |
| 36 | -0.358 | -0.632 to +0.634 | +0.025 | -0.049 to +0.052 | +0.963 | +0.994 | 97% |
| 41 | -0.283 | -0.407 to +0.401 | -0.006 | -0.041 to +0.043 | +0.964 | +0.988 | 100% |
| 47 | +0.108 | -0.330 to +0.328 | -0.005 | -0.050 to +0.055 | +0.921 | +0.982 | 100% |

## Credit - Gain (the "you" in a gain), against UBS: gain + you - gain

| Layer | Cosine | Null, 95% range | Cosine, dimensions on one scale | Null, 95% range | Emotion direction, two halves of the documents | UBS direction, two halves of the careers | Held out: documents sorted right |
|---|---|---|---|---|---|---|---|
| 6 | -0.082 | -0.289 to +0.284 | +0.062 | -0.063 to +0.067 | +0.964 | +0.993 | 100% |
| 12 | -0.054 | -0.286 to +0.284 | +0.062 | -0.062 to +0.062 | +0.959 | +0.948 | 100% |
| 18 | -0.732 | -0.776 to +0.777 | +0.015 | -0.024 to +0.025 | +0.980 | +0.983 | 97% |
| 24 | -0.216 | -0.779 to +0.780 | +0.016 | -0.032 to +0.031 | +0.787 | +0.994 | 88% |
| 31 | +0.094 | -0.381 to +0.371 | +0.023 | -0.035 to +0.034 | +0.940 | +0.980 | 100% |
| 36 | +0.051 | -0.355 to +0.354 | +0.043 | -0.054 to +0.057 | +0.930 | +0.979 | 100% |
| 41 | +0.015 | -0.171 to +0.174 | +0.019 | -0.041 to +0.042 | +0.902 | +0.969 | 100% |
| 47 | -0.278 | -0.383 to +0.382 | -0.011 | -0.040 to +0.039 | +0.935 | +0.976 | 100% |

## The drift: B's loss-framed careers minus its gain-framed careers along the Loss - Gain emotion direction, request by request (in units of the documents' own Loss - Gain gap along it)

| Request | Layer 6 | Layer 12 | Layer 18 | Layer 24 | Layer 31 | Layer 36 | Layer 41 | Layer 47 |
|---|---|---|---|---|---|---|---|---|
| 2011-01-07 (p344_i_can_hunt_with_u) | +0.024 | +0.100 | -0.043 | -0.068 | +0.003 | +0.048 | +0.037 | +0.025 |
| 2011-01-12 (p316_bust_through_it) | +0.009 | +0.032 | +0.283 | -0.145 | -0.085 | -0.071 | -0.115 | -0.001 |
| 2011-04-01 (p252_screw_other_people_harder) | +0.014 | +0.158 | +0.103 | -0.178 | -0.148 | -0.144 | -0.153 | +0.039 |
| 2011-06-08 (p250_grow_our_mafia) | +0.022 | +0.056 | -0.264 | -0.380 | -0.209 | -0.161 | -0.118 | +0.033 |
| 2011-06-08 (p317_stop_busters) | -0.000 | +0.031 | -0.088 | -0.371 | -0.133 | -0.138 | -0.120 | +0.056 |
| 2011-08-05 (p253_11_oclock_rule) | +0.028 | +0.027 | -0.416 | +0.006 | -0.100 | -0.114 | -0.078 | +0.090 |
