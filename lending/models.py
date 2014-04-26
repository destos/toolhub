from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
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
        RETURNED_DAMAGED: 'returned_damaged'
    }
    LENDING_ACTION_TEXT = {
        'requested': 'Requested Tool',
        'lent': 'Lent Tool',
        'recieved': 'Recieved Tool',
        'returned': 'Returned Tool',
        'lost': 'Lost Tool',
        'returned_damaged': 'Returned Tool Damaged'
    }
    RETURN_ACTIONS = (RETURNED, RETURNED_DAMAGED,)
    NEGATIVE_RETURN_ACTIONS = (RETURNED_DAMAGED, LOST,)
    CLOSING_ACTIONS = (RETURNED, RETURNED_DAMAGED, LOST,)
    ACTIVE_ACTIONS = (REQUESTED, LENT, RECIEVED,)
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

    def action_key(self):
        return self.LENDING_ACTIONS[self.action]

    def action_text(self):
        return self.LENDING_ACTION_TEXT[self.action_key()]


class TransactionManager(models.Manager):
    pass
    # TODO: see if this is even possible to do via a query
    # def active(self):
    #     return self.get_query_set().filter(
    #         history__action__in=LendingAction.ACTIVE_ACTIONS).latest(
    #             'history__created')


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
        return self.history.filter(action__in=LendingAction.CLOSING_ACTIONS)

    #TODO: on creation attach a new request action
