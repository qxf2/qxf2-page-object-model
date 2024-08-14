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
"image_path": "./screenshots/test_weather_shopper_payment_app/navigate_to_email_field.png",
"substring": "Invalid email address"
}

invalid_cardnum_in_payment_details = {
"card_type": "Credit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890",
"card_expiry": "12/25",
"card_cvv": "123",
"image_path": "./screenshots/test_weather_shopper_payment_app/navigate_to_cardnumber_field.png",
"substring": "Invalid card number"    
}

invalid_expirydate_in_payment_details = {
"card_type": "Debit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890123456",
"card_expiry": "25",
"card_cvv": "123",
"image_path": "./screenshots/test_weather_shopper_payment_app/navigate_to_cardexpiry_field.png",
"substring": "Invalid expiry date"    
}

invalid_cvv_in_payment_details = {
"card_type": "Credit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890123456",
"card_expiry": "12/25",
"card_cvv": "12",
"image_path": "./screenshots/test_weather_shopper_payment_app/navigate_to_cardcvv_field.png",
"substring": "Invalid cvv"
}

invalid_futuredate_in_payment_details = {
"card_type": "Debit Card",
"email": "qxf2tester@example.com",
"card_number": "1234567890123456",
"card_expiry": "12/2",
"card_cvv": "123",
"image_path": "./screenshots/test_weather_shopper_payment_app/navigate_to_futuredate_field.png",
"substring": "Expiration date"    
}
