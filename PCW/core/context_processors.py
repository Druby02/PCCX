from . forms import CurrencyForm
from currency_converter import CurrencyConverter

def currency_form(request):
    selected_currency = request.session.get("currency", "NOK")
    forexhate_currencies = CurrencyConverter().currencies

    form = CurrencyForm(initial={"currency": selected_currency})

    choices = []
    for currency in sorted(forexhate_currencies):
        choices.append((currency, currency))

    form.fields["currency"].choices = choices
    
    return {
        "currency_form": form
        }