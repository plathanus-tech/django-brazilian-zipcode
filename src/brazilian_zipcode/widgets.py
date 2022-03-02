from django.forms import widgets
from django.utils.safestring import mark_safe


class AutoBrazilianZipCodeInput(widgets.TextInput):
    def render(self, name, value, attrs, renderer):
        attrs["meta_id"] = "meta_zipcode_info"
        return super().render(name, value, attrs, renderer)

    class Media:
        js = ("getAddressInfo.js",)
