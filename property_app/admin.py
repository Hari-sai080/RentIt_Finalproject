from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Profile, Property, Notification, Amenity, PropertyImage, Review

admin.site.register(Profile)
admin.site.register(Property)
admin.site.register(Notification)
admin.site.register(Amenity)
admin.site.register(PropertyImage)
admin.site.register(Review)

# Create groups and assign permissions
def create_groups_and_permissions():
    tenant_group, created = Group.objects.get_or_create(name='Tenant')
    owner_group, created = Group.objects.get_or_create(name='Owner')
    agent_group, created = Group.objects.get_or_create(name='Agent')

    # Assign permissions to groups
    content_type = ContentType.objects.get_for_model(Property)
    permission = Permission.objects.get(codename='add_property', content_type=content_type)
    owner_group.permissions.add(permission)
    agent_group.permissions.add(permission)

    permission = Permission.objects.get(codename='change_property', content_type=content_type)
    owner_group.permissions.add(permission)
    agent_group.permissions.add(permission)

    permission = Permission.objects.get(codename='delete_property', content_type=content_type)
    owner_group.permissions.add(permission)
    agent_group.permissions.add(permission)

create_groups_and_permissions()