OTP_STATUS = {
    "sent": {'status': 'success', 'details': 'OTP sent successfully.'},
    "not_sent": {'status': 'failed', 'details': 'We could not send OTP. Please try again.'},
    "ignored": {'status': 'success', 'details': 'OTP has already been sent.'},
    "verified": {'status': 'success', 'details': 'OTP verified successfully'},
    "verification_failed": {'status': 'failed', 'details': 'Incorrect OTP, Please try again.'}
}

# {0} = api_key, {1} = customer's mobile number
TWO_FACTOR_OTP_REQUEST_URL = 'https://2factor.in/API/V1/{0}/SMS/+91{1}/AUTOGEN/OTP_Template'

# {0} = api_key, {1} = OTP session ID returned by Two factor, {2} = otp to be verified
TWO_FACTOR_OTP_VERIFICATION_URL = 'https://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}'
