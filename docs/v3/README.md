# ChatSecure Push Protocol Version 3

This document describes a privacy-conscious and federated way to wake up sleepy clients to establish new OTR sessions between app developers.

## Definitions

For the purposes of this document you are assumed to be Alice and your buddy is assumed to be Bob.

* `protocol` - Medium for messages such as XMPP or AIM. Example: "xmpp"
* `account_name` - Your account name on specified protocol. Example: alice@example.com
* `buddy_name` - Your friend's account name on protocol Example: bob@example.com
* `push_name` - Push username on specific push server / endpoint. Example: "bob"
* `api_endpoint` - Endpoint for instance of push server. Example: "push.chatsecure.org/api/v1/"
* `push_token` - Device-specific unique push token. Example: APNS token.
* `knock` - Message designed to wake device and establish new OTR session.
* `shared_key` - Symmetric key shared between Bob and Alice.

## Register Alice with App's Push Server

1. Create or login account with desired `push_name` and `password` w/ OAuth. `email_address` is optional during account creation and used for password recovery.
2. Optional: Fund `push_name` with in-app purchase or 'anonymously' via Bitcoin.
3. Register `push_token` with `push_name`.

## Initial Exchange over OTR TLV

1. Ask user to initiate Push handshake. If yes, continue.
2. Alice sends Bob `push_name` and `api_endpoint`.
3. Bob sends Alice `push_name` and `api_endpoint`.
4. Generate OTRv3's out of band `shared_key`, and store it securely on each client with:
	* Alice's `protocol`
	* Alice's `account_name`
	* Alice's `push_name`
	* Alice's `api_endpoint`
	* Bob's `buddy_name`
	* Bob's `push_name`
	* Bob's `api_endpoint`

## Sending Knock to Offline Contact

1. If Bob is offline, create a `knock` with the following info:
	* To: Bob's `api_endpoint` and Bob's `push_name`
	* From: Alice's `api_endpoint` and Alice's `push_name`
	* Encrypted with `shared_key`: 
		* `protocol`
		* Alice's `account_name`
		* Bob's `buddy_name`
2. Send full payload to Alice's `api_endpoint`.

## Server-to-Server Communication

1. Alice's `api_endpoint` receives `knock` from Alice.
2. Verify that Bob's `api_endpoint` has registered with Alice's `api_endpoint`, if same endpoint, skip this step and continue to Server-to-Client Communication.
3. Send `knock` to Bob's `api_endpoint`.

## Server-to-Client Communication

1. `knock` received and uses Bob's `push_name` to look up every `push_token` associated with Bob's account.
2. Send push notification with `knock` to every `push_token`.

## Receiving Knock

1. Look up `shared_key` from the 'public' To/From information in the knock.
2. Decrypt the encrypted information in the knock to determine which `protocol` and `account_name` to login, and which `buddy_name` to establish a new OTR session.
3. Login with `account_name` for `protocol`.
4. Establish new OTR session with `buddy_name` and generate and exchange new `shared_key`.
5. Exchange secure messages. Yay!