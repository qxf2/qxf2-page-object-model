valid_payment_details = {
"card_type": "Debit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890123456",
"card_expiry": "12/25",
"card_cvv": "123"
}

# Defining dictionaries with invalid field entries

invalid_email_in_payment_details = {
"card_type": "Debit Card",
"email": "qxf2tester",
"card_number": "1234567890123456",
"card_expiry": "12/25",
"card_cvv": "123",
"image_name": "navigate_to_email_field",
"validation_message": "Invalid email address"
}

invalid_cardnum_in_payment_details = {
"card_type": "Credit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890",
"card_expiry": "12/25",
"card_cvv": "123",
"image_name": "navigate_to_cardnumber_field",
"validation_message": "Invalid card number"
}

