from home_buying_app.decision import should_buy_home

def test_should_buy_home():
    assert should_buy_home(50000, 180000, 4) == "Yes, it's a good decision."
    assert should_buy_home(50000, 250000, 6) == "No, consider waiting or finding a cheaper option."