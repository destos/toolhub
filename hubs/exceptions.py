class OwnershipRequired(Exception):
    """
    Exception to raise if the owner is being removed before the hub.
    """
    pass


class HubMismatch(Exception):
    """
    Exception to raise if an hub user from a different hub is assigned
    to be an hub's owner.
    """
    pass
