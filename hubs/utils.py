from .models import Hub, HubUser, HubOwner


def create_hub(user, name, slug, is_active=True):
    """
    Returns a new hub, also creating an initial hub user who
    is the owner.
    """
    hub = Hub.objects.create(name=name, slug=slug, is_active=is_active)
    new_user = HubUser.objects.create(hub=hub, user=user, is_admin=True)
    HubOwner.objects.create(hub=hub, hub_user=new_user)
    return hub


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)
