from app.optimization.simulator import what_if

def test_simulator():
    result = what_if(100, 4, 10, True)
    assert result["optimized_cost"] < result["current_cost"]
    assert result["saving"] > 0
