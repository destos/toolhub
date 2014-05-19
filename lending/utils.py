from .models import LendingAction


def new_lending_action(
        transaction=None, action=LendingAction.REQUESTED, **kwargs):
    action = LendingAction.objects.create(
        transaction=transaction, action=action, **kwargs)
    transaction.last_action = action
    return action
