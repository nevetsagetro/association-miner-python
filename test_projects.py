import pytest
import pandas as pd
from project import get_baskets, calculate_support, generate_rules

def test_get_baskets():
    # Creamos un DataFrame de prueba
    data = {
        "transaction_id": [1, 1, 2, 3, 3],
        "product": ["milk", "bread", "milk", "apple", "bread"]
    }
    df = pd.DataFrame(data)
    baskets = get_baskets(df, "transaction_id", "product")
    
    assert len(baskets) == 3
    assert frozenset(["milk", "bread"]) in baskets
    assert frozenset(["apple", "bread"]) in baskets

def test_calculate_support():
    baskets = [
        frozenset(["milk", "bread"]),
        frozenset(["milk"]),
        frozenset(["bread", "apple"]),
    ]
    # "milk" aparece en 2 de 3
    assert calculate_support(baskets, frozenset(["milk"])) == pytest.approx(0.666, 0.01)
    # "milk" y "bread" juntos en 1 de 3
    assert calculate_support(baskets, frozenset(["milk", "bread"])) == pytest.approx(0.333, 0.01)
    # Algo que no existe
    assert calculate_support(baskets, frozenset(["beer"])) == 0

