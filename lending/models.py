from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
# from django.db.models import Q

from django_extensions.db.models import TimeStampedModel


class LendingAction(TimeStampedModel):
    REQUESTED = 0
    LENT = 1
    RECIEVED = 2
    RETURNED = 3
    LOST = 4
    RETURNED_DAMAGED = 5
    LENDING_ACTIONS = {
        REQUESTED: 'requested',
        LENT: 'lent',
        RECIEVED: 'received',
        RETURNED: 'returned',
        LOST: 'lost',
        RETURNED_DAMAGED: 'returned-damaged'
    }
    LENDING_ACTION_TEXT = {
        'requested': _('Requested Tool'),
        'lent': _('Lent Tool'),
        'recieved': _('Recieved Tool'),
        'returned': _('Returned Tool'),
        'lost': _('Lost Tool'),
        'returned-damaged': _('Returned Tool Damaged')
    }
    REQUEST_ACTIONS = (REQUESTED,)
    RETURN_ACTIONS = (RETURNED, RETURNED_DAMAGED,)
    NEGATIVE_RETURN_ACTIONS = (RETURNED_DAMAGED, LOST,)
    CLOSING_ACTIONS = (RETURNED, RETURNED_DAMAGED, LOST,)
    ACTIVE_ACTIONS = (LENT, RECIEVED,)
    LENDING_CHOICES = zip(LENDING_ACTIONS.keys(), LENDING_ACTIONS.values())
    transaction = models.ForeignKey(
        'Transaction',
        blank=False, null=False, related_name='history')
    action = models.IntegerField(choices=LENDING_CHOICES, default=0)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '%s, %s to %s' % (
            self.action_text(), self.transaction.tool, self.transaction.lendee)

    @property
    def action_key(self):
        return self.LENDING_ACTIONS[self.action]

    def action_text(self):
        return self.LENDING_ACTION_TEXT[self.action_key]


class TransactionQueryset(models.query.QuerySet):
    def action_group_filter(self, actions):
        assert isinstance(actions, (list, tuple))
        return self.filter(last_action__action__in=actions)

    def request_open(self):
        return self.action_group_filter(LendingAction.REQUEST_ACTIONS)

    def closed(self):
        return self.action_group_filter(LendingAction.CLOSING_ACTIONS)

    def active(self):
        return self.action_group_filter(LendingAction.ACTIVE_ACTIONS)


class TransactionManager(models.Manager):
    def get_query_set(self):
        return TransactionQueryset(self.model, using=self._db)

    def request_open(self):
        return self.get_query_set().request_open()

    def closed(self):
        return self.get_query_set().closed()

    def active(self):
        return self.get_query_set().active()


# TODO, adding a new action changes modified date
class Transaction(TimeStampedModel):
    """
    records one lending request from beginning to end
    """
    purpose = models.TextField()
    hub = models.ForeignKey(
        'hubs.Hub',
        blank=False, null=False, default=None, related_name='transactions')
    tool = models.ForeignKey(
        'tools.UserTool',
        related_name='lending_transactions',
        blank=False, null=False, default=None)
    lendee = models.ForeignKey(User, blank=False, null=False)
    last_action = models.ForeignKey(
        LendingAction, blank=True, null=True, related_name='latest_action')

    objects = TransactionManager()

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '%s, %s to %s' % (
            self.tool.tool_type, self.tool.owner, self.lendee)

    @property
    def lender(self):
        return self.tool.owner

    @property
    def closed(self):
        return self.get_closing_action().exists()

    def get_closing_action(self):
        return self.history.filter(
            action__in=LendingAction.CLOSING_ACTIONS).get()

    def get_absolute_url(self):
        return reverse('lending:transaction_progress',
                       kwargs=dict(transaction_id=self.id))
