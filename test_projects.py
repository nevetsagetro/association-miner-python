import pytest
import pandas as pd
from project import load_data, get_baskets, calculate_support, generate_rules

def test_load_data_error():
    """Verifica que el programa falle si el archivo no existe."""
    with pytest.raises(FileNotFoundError):
        load_data("data/non_existent_file.csv")

def test_get_baskets():
    """Verifica que el agrupamiento por transacciones funcione."""
    df = pd.DataFrame({
        "transaction_id": [1, 1, 2],
        "product": ["Milk", "Bread", "Milk"]
    })
    baskets = get_baskets(df, "transaction_id", "product")
    assert len(baskets) == 2
    assert "Milk" in baskets[0]
    assert "Bread" in baskets[0]
    assert isinstance(baskets[0], frozenset)

def test_generate_rules():
    """Verifica que se generen reglas cuando hay asociaciones claras."""
    # En este set, siempre que hay A, hay B (Confianza 1.0)
    baskets = [frozenset(["A", "B"]), frozenset(["A", "B"]), frozenset(["C"])]
    rules = generate_rules(baskets, min_support=0.1)
    
    assert not rules.empty
    # Verificar que el Lift sea mayor a 1 (A y B están correlacionados)
    assert rules.iloc[0]['lift'] > 1