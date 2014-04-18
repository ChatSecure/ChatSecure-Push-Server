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
* `whitelist_token` - token used for the push server to identify the correct `push_name`. Each token is unique to a given `buddy_name` and `account_name` and is refreshed periodically.

## Register Alice with App's Push Server

1. Create or login account with desired `push_name` and `password` w/ OAuth. `email_address` is optional during account creation and used for password recovery.
2. Optional: Fund `push_name` with in-app purchase or 'anonymously' via Bitcoin.
3. Register `push_token` with `push_name`.
4. Request bulk list of valid `whitelist_token`s and store on device

## Initial Exchange over OTR TLV

1. Ask user to initiate Push handshake. If yes, continue.
2. Alice sends Bob a `whitelist_token` and `api_endpoint`.
3. Bob sends Alice a `whitelist_token` and `api_endpoint`.
4. Generate OTRv3's out of band `shared_key`, and store it securely on each client with:
	* Alice's `protocol`
	* Alice's `account_name`
	* Alice's `push_name`
	* Alice's `whitelist_token`
	* Alice's `api_endpoint`
	* Bob's `buddy_name`
	* Bob's `whitelist_token`
	* Bob's `api_endpoint`

## Sending Knock to Offline Contact

1. If Bob is offline, create a `knock` with the following info:
	* To: Bob's `api_endpoint` and Bob's `whitelist_token`
	* timestamp: `yyyy-MM-dd HH:mm:ss`
	* HMAC-SHA-256 signature
2. Send full payload to Alice's `api_endpoint`.

## Server-to-Server Communication

1. Alice's `api_endpoint` receives `knock` from Alice.
2. Verify that Bob's `api_endpoint` has registered with Alice's `api_endpoint`, if same endpoint, skip this step and continue to Server-to-Client Communication.
3. Send `knock` to Bob's `api_endpoint`.

## Server-to-Client Communication

1. `knock` received and uses Bob's `whitelist_token` to look up every `push_token` associated with Bob's `push_name`.
2. Send push notification with `knock` to every `push_token`.

## Receiving Knock

1. Look up `shared_key` from the 'public' From `whitelist_token` information in the knock.
2. Verify the HMAC-SHA-256 signature.
3. Look up associated `account_name`, `protocol` and `buddy_name` for the `whitelist_token`
3. Login with `account_name` for `protocol`.
4. Establish new OTR session with `buddy_name` and generate and exchange new `shared_key` and `whitelist_token`.
5. Exchange secure messages. Yay!