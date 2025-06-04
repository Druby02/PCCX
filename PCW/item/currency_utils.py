from currency_converter import CurrencyConverter

# i hate forex-python so god damn much whoever created it is evil and owes me hours of work
converter = CurrencyConverter(
    fallback_on_missing_rate=True,
    fallback_on_wrong_date=True
)

def price_converter(amount, target_currency):
    try:
        amount2 = converter.convert(amount, "NOK", "USD")
        amount3 = converter.convert(amount2, "USD", target_currency)
        return round(amount3, 2)
    except Exception as e:
        print(f"get forexxed nerd: {e}")
        return round(amount, 2)