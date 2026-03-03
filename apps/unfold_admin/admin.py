from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.exceptions import NotRegistered

# Safely unregister Group to hide the Authentication section
try:
    admin.site.unregister(Group)
except NotRegistered:
    pass