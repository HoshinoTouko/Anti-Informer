# API

## Overview

This document is a design reference of server api. All development must be the same to this.

### Key protocol (/key)

#### User

##### POST: /user/register

```
payload: {
    name: username(Cannot repeat),
    public_key: user_public_key
},
signature: sign(payload)
```

res

```
payload: {
    encrypt_session_key,
    ciphertext,
    tag
},
signature: signature(payload)
```

#### Session

##### POST: /session/start

```
payload: {
    user: username
}
```

res

```
payload: {
    key
},
signature: signature(payload)
```

Server will generate a session and delete exist session with server signature.

Next time when client ask for his message or send something to other, he has to append the session key to the message signature.

The token is disposable.
