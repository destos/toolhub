# Hub's borrow heavily from django-organization
from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class HubQueryset(models.query.QuerySet):

    def enabled(self):
        return self.filter(is_enabled=True)

    def disabled(self):
        return self.filter(is_enabled=False)

    def private(self):
        return self.filter(is_private=True)

    def public(self):
        return self.filter(is_enabled=True, is_private=False)

    def get_for_user(self, user):
        return self.filter(users=user)


class HubManager(models.Manager):

    def get_query_set(self):
        return HubQueryset(self.model, using=self._db)

    def get_for_user(self, user):
        return self.get_query_set().get_for_user(user)


class PublicHubManager(HubManager):
    """
    A more useful extension of the default manager which returns querysets
    including only enabled and public hubs
    """

    def get_query_set(self):
        return super(
            PublicHubManager, self).get_query_set().public()


class Hub(TimeStampedModel):
    """
    Handles relations to different users and their shared tools

    An hub can have multiple users but only one who can be designated
    the owner user.

    """
    name = models.CharField(
        max_length=200,
        help_text=_("The name of the hub"))
    slug = AutoSlugField(
        max_length=200, blank=False, editable=True, populate_from='name',
        unique=True)
    users = models.ManyToManyField(USER_MODEL, through="HubUser")
    is_enabled = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    objects = HubManager()
    public = PublicHubManager()

    class Meta:
        ordering = ['name']
        verbose_name = _("hub")
        verbose_name_plural = _("hubs")

    def __unicode__(self):
        return self.name

    # TODO: add more permalinks to be used throughout the templates
    @permalink
    def get_absolute_url(self):
        return ('hubs:detail', (), {'hub_slug': self.slug})

    @permalink
    def get_edit_url(self):
        return ('hubs:edit', (), {'hub_slug': self.slug})

    def add_user(self, user, is_admin=False):
        """
        Adds a new user and if they are the first user makes the user an
        admin and the owner. """
        users_count = self.user_count
        if users_count == 0:
            is_admin = True
        hub_user = HubUser.objects.create(
            user=user, hub=self, is_admin=is_admin)
        if users_count == 0:
            HubOwner.objects.create(
                hub=self, hub_user=hub_user)
        return hub_user

    def get_or_add_user(self, user, is_admin=False):
        """
        Adds a new user to the hub, and if it's the first user makes
        the user an admin and the owner. Uses the `get_or_create` method to
        create or return the existing user.
        `user` should be a user instance, e.g. `auth.User`.

        Returns the same tuple as the `get_or_create` method, the
        `HubUser` and a boolean value indicating whether the
        HubUser was created or not.
        """
        users_count = self.user_count
        if users_count == 0:
            is_admin = True
        hub_user, created = HubUser.objects.get_or_create(
            hub=self, user=user, defaults={'is_admin': is_admin})
        if users_count == 0:
            HubOwner.objects.create(
                hub=self, hub_user=hub_user)

        return hub_user, created

    @property
    def user_count(self):
        return self.users.all().count()

    def is_member(self, user):
        return self.hub_users.filter(user=user).exists()

    def is_admin(self, user):
        return True if self.hub_users.filter(
            user=user, is_admin=True) else False


class HubUser(TimeStampedModel):
    """
    ManyToMany through field relating Users to Hub.

    It is possible for a User to be a member of multiple hubs, so this
    class relates the HubUser to the User model using a ForeignKey
    relationship, rather than a OneToOne relationship.

    Authentication and general user information is handled by the User class
    and the contrib.auth application.

    """
    user = models.ForeignKey(USER_MODEL, related_name="hub_users")
    hub = models.ForeignKey(Hub, related_name="hub_users")
    is_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ['hub', 'user']
        unique_together = ('user', 'hub')
        verbose_name = _("hub user")
        verbose_name_plural = _("hub users")

    def __unicode__(self):
        return u"%s (%s)" % (self.name if self.user.is_active else (
            self.user.email), self.hub.name)

    def delete(self, using=None):
        """
        If the hub user is also the owner, this should not be deleted
        unless it's part of a cascade from the Hub.

        If there is no owner then the deletion should proceed.
        """
        from .exceptions import OwnershipRequired
        try:
            if self.hub.owner.hub_user.id == self.id:
                raise OwnershipRequired(_("Cannot delete hub owner before"
                                          " hub or transferring ownership."))
        except HubOwner.DoesNotExist:
            pass
        super(HubUser, self).delete(using=using)

    @permalink
    def get_absolute_url(self):
        return ('hubs:user_detail', (),
                {'hub_slug': self.hub.slug,
                 'user_username': self.user.username})

    @property
    def name(self):
        if hasattr(self.user, 'get_full_name'):
            return self.user.get_full_name()

        return "%s" % self.user


class HubOwner(TimeStampedModel):
    """Each hub must have one and only one hub owner."""

    hub = models.OneToOneField(Hub, related_name="owner")
    hub_user = models.OneToOneField(
        HubUser, related_name="owned_hub")

    class Meta:
        verbose_name = _("hub owner")
        verbose_name_plural = _("hub owners")

    def __unicode__(self):
        return u"%s: %s" % (self.hub, self.hub_user)

    def save(self, *args, **kwargs):
        """
        Extends the default save method by verifying that the chosen
        hub user is associated with the hub.

        """
        from .exceptions import HubMismatch
        if self.hub_user.hub != self.hub:
            raise HubMismatch
        else:
            super(HubOwner, self).save(*args, **kwargs)
