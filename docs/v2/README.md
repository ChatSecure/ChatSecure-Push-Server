# ChatSecure Push API v2

This is a redesign to make everything simpler.

### POST /api/account

Parameters:
	
* `email` - Required
* `password` - Required

Results:

* Creates new account with desired email and password.

### POST /api/device

Parameters:

* `operating_system` - Device operating system
* `device_type` - Device manufacturer
* `apple_push_token` - APNS token

Results:

* Creates new device or updates existing device and attaches it to the user's account.




