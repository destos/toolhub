from django.conf.urls import url, patterns

from . import views

# namespaced under lending
urlpatterns = patterns(
    '',
    url(r'^new/(?P<hub_slug>[-_\w]+)/(?P<usertool_id>\d+)/$',
        views.StartTransactionView.as_view(),
        name='new_transaction'),
    url(r'^progress/(?P<transaction_id>\d+)/$',
        views.TransactionProgressView.as_view(),
        name='transaction_progress'),
)
