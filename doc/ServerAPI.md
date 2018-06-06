# API

## Overview

This document is a design reference of server api. All development must be the same to this.

### Key protocol (/key)

#### Key register (New user register) (/upload)

##### Start

POST [\[/start\]](KeyProtocol.md/#send-pk-to-server) - 1

TODO: A new `auth_code` generator should be designed.

##### Register

POST: [\[/register\]](KeyProtocol.md/#send-pk-to-server) - 5

TODO: Check digital signature

#### Key exchange (/exchange)

##### Get all public

GET: [\[/public/all\]](KeyProtocol.md/#request-others-pk)

##### Get public by username

GET: [\[/public\]](KeyProtocol.md/#request-others-pk)
params: username


