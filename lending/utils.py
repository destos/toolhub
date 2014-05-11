from .models import LendingAction


def new_lending_action(
        transaction=None, action=LendingAction.REQUESTED, **kwargs):
    return LendingAction.objects.create(
        transaction=transaction, action=action, **kwargs)
