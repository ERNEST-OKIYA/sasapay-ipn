
from django.db import transaction
from django.utils.decorators import method_decorator

#create global transactional class mixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from notifications.models import Message


class TransactionalViewMixin(object):
    """This is a global view wrapper that provides ,
    transactions and filters
    """
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)



    def perform_destroy(self,model_object):
        """ called by generic detail view for flagging is_deleted to True.
        """

        model_object.is_deleted=True
        model_object.save()

    def send_email(self,message,recipient,template_id=None,subject=None):
        return Message.create_email(message=message,recipient_address=recipient,
                                    template_id=template_id,subject=subject)

    # def send_sms(self,message,recipient):
    #     return Message.create_sms(message=message,recipient_address=recipient)

    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(TransactionalViewMixin, self).dispatch(*args, **kwargs)