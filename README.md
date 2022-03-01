# Django-Brazilian-Zipcode

This [Django](https://www.djangoproject.com/) add-in lib aims to make easy to wrap an external service for querying an [ZipCode (CEP)](https://pt.wikipedia.org/wiki/C%C3%B3digo_de_Endere%C3%A7amento_Postal). By default uses the [Correios public API](https://buscacepinter.correios.com.br/app/endereco/index.php) to retrieve the address info. You can also use your own API, Database, or service to retrieve addresses.
In the future, we seek to add an autocomplete widget to the admin site.

## Installation

> pip install django-brazilian-zipcode

## Usage

### On a Form, as an Field

```python
# your_app/forms.py
from django import forms
from brazilian_zipcode import BrazilianZipCodeField


class YourForm(forms.Form):
    zipcode_info = BrazilianZipCodeField()

```

```python
# your_app/views.py
from django.http import HttpRequest
from brazilian_zipcode import BrazilianAddress
from your_app.forms import YourForm


def your_view(request: HttpRequest):
    form = YourForm(data=request.POST)
    form.is_valid(raise_exception=True)

    form.zipcode_info # This attr is an instance of: `BrazilianAddress`
    print(form.zipcode_info.street)
    print(form.zipcode_info.zipcode)
    print(form.zipcode_info.district)
    print(form.zipcode_info.city)
    print(form.zipcode_info.state_initials)
    
    ...
```

### As an API

On your project `urls.py` include the brazilian_zipcode urls to your `urlpatterns`:

```python
# your_project.urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path("", include("brazilian_zipcode.urls")),
    ...
]
```

This will expose a route to query addresses on: `/api/address_info`.
You can then make a GET request to the endpoint passing the desired address as a query parameter like: `/api/address_info?zipcode=12345678`

That returns a `JSON` like:

```json
{
    "zipcode": "12345678",
    "street": "The street",
    "district": "The district",
    "city": "The City",
    "state_initials": "UF"
}
```

If the service is unavailable, you may receive a 404 response.

### Writing your own Address Retrieve Service

To provide your own service for retrieving addresses, you should:

1; Create a Class that implements an `classmethod` called `get_address_info`:

```python
from brazilian_zipcode import BrazilianAddress


class YourAddressRetrievingService:

    @classmethod
    def get_address_info(cls, address: str) -> BrazilianAddress:
        ...
```

2; This method should return an instance of `BrazilianAddress`:

```python
class YourAddressRetrievingService:

    @classmethod
    def get_address_info(cls, address: str) -> BrazilianAddress:
        
        # Get the information on an database, external service...
        ...

        return BrazilianAddress(
            zipcode="Your ZipCode",
            street="Your Street",
            district="Your District",
            city="Your City",
            state_initials="Your State Initials
        )

```

3; Provide the absolute importable path to your class on your_project `settings.py`:

```python
# your_project.settings.py

# Other settings...
...

ADDRESS_PARSER_CLASS = "your_app.module.YourAddressRetrievingService"

```
