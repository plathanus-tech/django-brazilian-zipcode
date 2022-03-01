from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    zipcode = serializers.CharField()
    street = serializers.CharField()
    district = serializers.CharField()
    city = serializers.CharField()
    state_initials = serializers.CharField()
