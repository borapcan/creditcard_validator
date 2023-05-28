from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from datetime import datetime

def index(request):
    return render(request, 'validator/index.html')

def validate_credit_card(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiration_month = request.POST.get('expiration_month')
        expiration_year = request.POST.get('expiration_year')
        cvv = request.POST.get('cvv')

        # Perform your credit card validation checks here
        try:
            # Check expiry date
            current_date = datetime.now()
            expiration_date = datetime(int(expiration_year), int(expiration_month), 1)  # Assuming day is always 1st
            if expiration_date <= current_date:
                raise ValidationError('Card has expired.')

            # Check CVV length
            card_type = 'amex' if card_number.startswith(('34', '37')) else 'non-amex'
            if (card_type == 'amex' and len(cvv) != 4) or (card_type == 'non-amex' and len(cvv) != 3):
                raise ValidationError('Invalid CVV length.')

            # Check PAN length
            if not 16 <= len(card_number) <= 19:
                raise ValidationError('Invalid PAN length.')

            # Check PAN using Luhn's algorithm (last digit)
            digits = [int(x) for x in str(card_number)]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            total = sum(odd_digits) + sum(sum(divmod(2 * digit, 10)) for digit in even_digits)
            if total % 10 != 0:
                raise ValidationError('Invalid PAN (failed Luhn\'s algorithm).')

            # If all validation checks pass, you can send a success response
            return HttpResponse('Validation successful! Credit card is valid.')

        except ValidationError as e:
            # If any validation check fails, you can send an error response
            return HttpResponse(f'Validation failed: {str(e)}')

    return render(request, 'validator/validator.html')  # Replace 'validator.html' with your actual template name
