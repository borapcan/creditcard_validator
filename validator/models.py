from django.db import models
from django.core.exceptions import ValidationError

class CreditCard(models.Model):
    CARD_TYPES = [
        ('visa', 'Visa'),
        ('master', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
        ('unknown', 'Unknown')
    ]

    card_number = models.CharField(max_length=19)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, default='unknown', editable=False)

    def save(self, *args, **kwargs):
        # Set the card_type based on the card_number prefix
        if self.card_number.startswith(('4', '5')):
            self.card_type = 'visa' if self.card_number.startswith('4') else 'master'
        elif self.card_number.startswith('34') or self.card_number.startswith('37'):
            self.card_type = 'amex'
        elif self.card_number.startswith('6'):
            self.card_type = 'discover'
        else:
            raise ValidationError('Unknown card issuer.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.card_type} - {self.card_number}"