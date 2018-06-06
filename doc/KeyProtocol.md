## Key Protocol

## Personal

### Generate key pair

KeyGen() -> `pk`, `sk`

#### Send pk to server

1. Ask server for an `auth_code`. Server will save the `auth_code` to database.
2. Append the `auth_code` to payload.
3. Generate a `payload`
```
{
    pk: pk,
    timestamp: timestamp,
    auth_code: auth_code
}
```
4. Send `payload` to `server`, use the template below:
```
{
    `payload`,
    signature: Signature(
        HASH(`payload`), `sk`
    )
}
```
5. Server respond. If the response correct, user will receive a data structure
```
payload:
{
    result: result,
    server_pk: server_pk,
    timestamp: timestamp
}
response:
{
    payload,
    signature: Signature(
        HASH(`payload`), `server_sk`
    )
}
```

#### Store

1. Ask user for a `password`.
2. Generate a data structure `userinfo`
```
{
    name: name,
    pk: pk,
    sk: sk
}
```
3. Store the `password` at local use AES(`userinfo`, `password`)

## Public

### Communicate

### Request all user's `pk`

1. Watch [Response](#response)
2. Auth response by pre-store server pk

### Request other's `pk`

1. Send params `username`
2. Watch [Response](#response)
3. Auth response by pre-store server pk

### Response

```
payload:
{
    pk: user_pk,
    timestamp: timestamp,
    auth_code: auth_code
}
response:
{
    payload,
    signature: Signature(
        HASH(`payload`), `server_sk`
    )
}
```
