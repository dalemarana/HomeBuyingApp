def should_buy_home(income, house_price, interest_rate):
    affordability = income * 4
    if house_price <= affordability and interest_rate < 5:
        return "Yes, it's a good decision."
    return "No, consider waiting or finding a cheaper option."