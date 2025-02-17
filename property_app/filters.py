from django_filters import FilterSet, NumberFilter, MultipleChoiceFilter
from .models import Property

class PropertyFilter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    amenities = MultipleChoiceFilter(
        field_name='amenities__name',
        choices=Property.AMENITY_CHOICES,
        conjoined=True
    )

    class Meta:
        model = Property
        fields = ['property_type', 'bedrooms', 'bathrooms']