from app.optimization.cost_engine import calculate_savings

def test_savings():
    result = calculate_savings(100, 75)
    assert result["saving"] == 25
    assert result["saving_percent"] == 25
    assert result["annual_saving"] == 300
