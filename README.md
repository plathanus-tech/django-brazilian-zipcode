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
from django.http import HttpRequest, HttpResponse
from brazilian_zipcode import BrazilianAddress
from your_app.forms import YourForm


def your_view(request: HttpRequest):
    form = YourForm(data=request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)

    zipcode_info = form.cleaned_date.get("zipcode_info")
    print(zipcode_info.street)
    print(zipcode_info.zipcode)
    print(zipcode_info.district)
    print(zipcode_info.city)
    print(zipcode_info.state_initials)
    
    return HttpResponse(status=200)
```

```python
# your_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    ...
    path('your_view/', views.your_view)
]
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


### As an Widget (Requires the API step)

You can use this widget to automatically show the address on the admin using the widget `AutoBrazilianZipCodeInput`.
After the user inputs the zipcode, it will make an get request to the API endpoint and displays the result directly on the admin.
Follow these steps:

1; Create your form:

```python
# your_app.forms.py

from django import forms
from brazilian_zipcode import BrazilianZipCodeField
from brazilian_zipcode.widgets import AutoBrazilianZipCodeInput
from your_app.models import YourModel


class MyAddressForm(forms.ModelForm):
    # Here we used ModelForm, but you can use any other form.

    zipcode_info = BrazilianZipCodeField(widget=AutoBrazilianZipCodeInput())

    class Meta:
        model = YourModel
        fields = ['zipcode_info']

```

2; Set the widget on the field:

```python
# your_app.forms.py

class MyAddressForm(forms.ModelForm):
    # Here we used ModelForm, but you can use any other form.

    zipcode_info = BrazilianZipCodeField(widget=AutoBrazilianZipCodeInput())
    # You can also use any other CharField you like
```

3; Set the form on the admin:

```python
# your_app.admin.py

from django.contrib import admin
from .models import Address
from .forms import MyAddressForm

# Register your models here.
@admin.register(Address)
class MyAdressAdmin(admin.ModelAdmin):
    form = MyAddressForm

```

4; Collect the required JavaScript:
> python3 manage.py collectstatic

### Writing your own Address Retrieve Service

You can also provide your custom service for retrieving addresses. This will be used on all use cases stated above.
To do so you should:

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


Enjoy! :D
