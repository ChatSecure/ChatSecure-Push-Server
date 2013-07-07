# ChatSecure Push API v2

This is a redesign to make everything simpler.

### POST /api/account

Parameters:
	
* `email` - (String) **Required**
* `password` - (String) **Required**
* `create` - (BOOL) *Optional* - Tries to create account.

Results:

* Create new or login existing account with given email and password.

### POST /api/device

Parameters:

* `operating_system` - Device operating system
* `device_type` - Device manufacturer
* `apple_push_token` - APNS token

Results:

* Creates new device or updates existing device and attaches it to the user's account.

### POST /api/knock

Parameters:

* `email` - (String) **Required**
* `whitelist_token` - (String) *Optional*

Results:

* Asynchronously schedules push messages to all registered devices tied to an email. This design could be abused by spammers, so an optional whitelist_token can be used.


