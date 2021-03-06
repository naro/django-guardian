from django.db.models import signals
from django.contrib.auth.models import User, Group
from guardian import models as guardian_app
from guardian.conf import settings as guardian_settings


def create_anonymous_user(sender, **kwargs):
    """
    Creates anonymous User instance with id from settings.
    """
    try:
        User.objects.get(pk=guardian_settings.ANONYMOUS_USER_ID)
    except User.DoesNotExist:
        User.objects.create(pk=guardian_settings.ANONYMOUS_USER_ID,
            username='AnonymousUser')


def create_authenticated_virtual_group(sender, **kwargs):
    """
    Creates group which acts as virtual group for all authenticated members
    """
    try:
        Group.objects.get(pk=guardian_settings.AUTHENTICATED_VIRTUAL_GROUP_ID)
    except Group.DoesNotExist:
        Group.objects.create(pk=guardian_settings.AUTHENTICATED_VIRTUAL_GROUP_ID,
            name=guardian_settings.AUTHENTICATED_VIRTUAL_GROUP_NAME)


signals.post_syncdb.connect(create_anonymous_user, sender=guardian_app,
    dispatch_uid="guardian.management.create_anonymous_user")

signals.post_syncdb.connect(create_authenticated_virtual_group, sender=guardian_app,
    dispatch_uid="guardian.management.create_authenticated_virtual_group")
