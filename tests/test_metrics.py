import numpy as np

from hfml.metrics import classification_metrics


def test_perfect_predictions():
    logits = np.array([[2.0, 0.1], [0.1, 3.0], [1.0, 0.0]])
    labels = np.array([0, 1, 0])
    m = classification_metrics((logits, labels))
    assert m["accuracy"] == 1.0
    assert m["f1_macro"] == 1.0
