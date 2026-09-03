# Week 3 — Authentication Concepts

## 1. Authentication

Authentication means proving who you are.

For example, when a user enters a username and password during login, the server checks whether the credentials are correct.

In simple words:

**Authentication = Who are you?**

---

## 2. Authorization

Authorization means deciding what an authenticated user is allowed to do.

For example, an Admin may be allowed to delete a book, while a normal user may only be allowed to view books.

In simple words:

**Authorization = What are you allowed to do?**

### Difference Between Authentication and Authorization

| Authentication                 | Authorization                        |
| ------------------------------ | ------------------------------------ |
| Verifies the user's identity   | Determines what the user can access  |
| Usually happens during login   | Happens after the user is identified |
| Example: Username and password | Example: Admin can delete books      |

---

## 3. Password Hashing

Passwords should never be stored as plain text in a database.

Instead, a password is converted into a one-way hash before it is stored.

The basic process is:

```text
Original Password
       ↓
   Hash Function
       ↓
Stored Password Hash
```

When the user logs in, the server checks the entered password against the stored password hash.

### What would happen if passwords were stored as plain text?

If the database was leaked or hacked, attackers could directly see the actual passwords of users.

They could then use those passwords to access the users' accounts. If a user used the same password on other websites, those accounts could also be at risk.

Therefore, storing passwords as plain text is unsafe. Password hashing helps protect users' passwords if the database is compromised.

---

## 4. JWT — JSON Web Token

JWT stands for **JSON Web Token**.

A JWT is a signed token that can be issued by a server after a user successfully logs in.

The client can send the JWT with future requests instead of sending the username and password again every time.

A JWT has three parts separated by dots:

```text
HEADER.PAYLOAD.SIGNATURE
```

---

## 5. Three Parts of a JWT

### 5.1 Header

The header contains information about the token, such as the signing algorithm and token type.

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Here:

* `alg` means the algorithm used to sign the token.
* `typ` means the token type, which is JWT.

---

### 5.2 Payload

The payload contains claims, which are pieces of information about the user or token.

Example:

```json
{
  "sub": "123",
  "name": "Eman",
  "role": "Admin"
}
```

Here:

* `sub` represents the user or subject ID.
* `name` represents the user's name.
* `role` represents the user's role.

---

### 5.3 Signature

The signature is used to verify that the JWT was created correctly and has not been changed.

The signature is the third part of the JWT.

It is not normally decoded as readable JSON.

---

## 6. JWT Example

Example JWT:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJuYW1lIjoiRW1hbiIsInJvbGUiOiJBZG1pbiJ9.example-signature
```

The JWT contains three parts:

### Part 1 — Header

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

Decoded header:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Part 2 — Payload

```text
eyJzdWIiOiIxMjMiLCJuYW1lIjoiRW1hbiIsInJvbGUiOiJBZG1pbiJ9
```

Decoded payload:

```json
{
  "sub": "123",
  "name": "Eman",
  "role": "Admin"
}
```

### Part 3 — Signature

```text
example-signature
```

The signature is used to verify the integrity and authenticity of the token.

**Important:** The JWT payload is encoded, not encrypted. Therefore, sensitive information such as passwords should never be stored inside a JWT payload.

---

## 7. Claims

Claims are pieces of information stored inside the JWT payload.

For example:

```json
{
  "sub": "123",
  "name": "Eman",
  "role": "Admin"
}
```

The claims in this example are:

* `sub` — identifies the user.
* `name` — contains the user's name.
* `role` — identifies the user's role.

Claims can be used by the server to make authorization decisions.

---

## 8. Role-Based Authorization

Role-based authorization means restricting access to certain actions based on the user's role.

For example:

```text
Admin → Can view, add, update, and delete books.

User → Can view books.
```

The user's role can be included as a claim in the JWT.

For example, if a user has:

```json
{
  "role": "Admin"
}
```

the server can allow that user to access an Admin-only endpoint.

For example:

```text
DELETE /api/Books/5
```

The server could allow this operation only to users with the `Admin` role.

---


## 9. Authentication Flow

The basic authentication flow is:

```text
Client
   |
   |  Login request
   |  Username + Password
   ↓
Server
   |
   |  Check password against stored hash
   |
   |  If valid
   ↓
Server
   |
   |  Issues JWT
   ↓
Client
   |
   |  Stores JWT
   |
   |  Sends JWT with next request
   ↓
Server
   |
   |  Validates JWT
   |
   |  Checks authorization
   ↓
Client
   |
   |  Receives response

```
## 9. Authentication Sequence Diagram

The following sequence shows how authentication works from login to a subsequent request:

```text
┌──────────────┐                         ┌──────────────┐
│    Client    │                         │    Server    │
└──────┬───────┘                         └──────┬───────┘
       │                                        │
       │  Login request                         │
       │  Username + Password                   │
       │───────────────────────────────────────>│
       │                                        │
       │                                        │
       │                              Check password hash
       │                                        │
       │                                        │
       │              JWT                       │
       │<───────────────────────────────────────│
       │                                        │
       │  Store JWT                             │
       │                                        │
       │                                        │
       │  Next request + JWT                    │
       │───────────────────────────────────────>│
       │                                        │
       │                              Validate JWT
       │                                        │
       │                              Check authorization
       │                                        │
       │              Response                  │
       │<───────────────────────────────────────│
       │                                        │
```

### Sequence Explanation

1. The client sends a login request containing a username and password.
2. The server checks the password against the stored password hash.
3. If the credentials are valid, the server issues a JWT.
4. The client stores the JWT.
5. The client sends the JWT with the next request.
6. The server validates the JWT.
7. The server checks whether the user is authorized to perform the requested action.
8. The server sends the response to the client.


### Flow in simple words

1. The client sends a login request with a username and password.
2. The server checks the password against the stored password hash.
3. If the credentials are correct, the server issues a JWT.
4. The client stores the JWT.
5. The client sends the JWT with the next request.
6. The server validates the JWT.
7. The server checks whether the user is authorized to perform the requested action.
8. The server sends a response to the client.

---

## 10. Summary

Authentication and authorization are different concepts.

**Authentication** verifies who the user is, while **authorization** determines what the user is allowed to do.

Passwords should never be stored as plain text. They should be stored using secure password hashing.

JWTs can be used to identify an authenticated user when making future API requests.

A JWT consists of three parts:

```text
Header.Payload.Signature
```

The payload contains claims such as the user ID and role.

Role-based authorization can use these claims to restrict access to specific actions, such as allowing only Admin users to delete books.
