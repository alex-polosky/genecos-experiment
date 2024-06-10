from ._base import BaseModel
from django.db import models
from django.utils.translation import gettext as _


class AccountStatus(models.IntegerChoices):
    '''Bit flags status for Account Status'''
    INACTVE = 0b1, _('Inactive')
    PAID_IN_FULL = 0b10, _('Paid in full')
    IN_COLLECTION = 0b100, _('In collection')


class Account(BaseModel):
    contract = models.ForeignKey('Contract', on_delete=models.PROTECT)

    # This is represented in the csv as -only- guid, but what if there's a client who utilizes some other id?
    client_reference = models.CharField(max_length=255, unique=True)

    # Money management is it's own whole can of worms.
    # TODO: expand debt_owed to allow different currencies, possibly utilizing a table of ISO 4217 codes and active dates to account for minor unit changes
    # As it is now, I think if an account owes >= $1b there's bigger problems?
    debt = models.DecimalField(max_digits=11, decimal_places=2)
    balance = models.DecimalField(max_digits=11, decimal_places=2)

    status = models.PositiveIntegerField(choices=AccountStatus)
