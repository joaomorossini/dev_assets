# API Reference: User

## Add a User

### Endpoint

**POST**  
`https://api.getz.`

### Request

This endpoint expects an object.

### Response

(No further details provided)

````bash
curl https://api.getz. \
> -H "Authorization: Api-Key <apiKey>"

```markdown
# Zep User API Reference

## Add a User
### Endpoint
`POST /api/v2/users`

### Request
This endpoint expects an object:
- **email** (string, Optional): The email address of the user.
- **fact_rating_instruction** (object, Optional): Optional instruction to use for fact rating.
- **first_name** (string, Optional): The first name of the user.
- **last_name** (string, Optional): The last name of the user.
- **metadata** (map from strings to any, Optional): The metadata associated with the user.
- **user_id** (string, Optional): The unique identifier of the user.

### Response
The user that was added:
- **created_at** (string, Optional)
- **deleted_at** (string, Optional)
- **email** (string, Optional)
- **fact_rating_instruction** (object, Optional)
- **first_name** (string, Optional)
- **id** (integer, Optional)
- **last_name** (string, Optional)
- **metadata** (map from strings to any, Optional)
- **project_uuid** (string, Optional)
- **session_count** (integer, Optional)
- **updated_at** (string, Optional)
- **user_id** (string, Optional)
- **uuid** (string, Optional)

### Errors
- **400**: User Add Request Bad Request Error
- **500**: User Add Request Internal Server Error

### Example
#### cURL
```bash
curl -X POST https://api.getzep.com/api/v2/users \
-H "Authorization: Api-Key <apiKey>" \
-H "Content-Type: application/json" \
-d '{}'

List All Users
Endpoint
GET /api/v2/users-ordered

Query Parameters
pageNumber (integer, Optional): Page number for pagination, starting from 1.
pageSize (integer, Optional): Number of users to retrieve per page.
Response
Successfully retrieved list of users:

row_count (integer, Optional)
total_count (integer, Optional)
users (list of objects, Optional)
Errors
400: User List Ordered Request Bad Request Error
500: User List Ordered Request Internal Server Error
Get a User
Endpoint
GET /api/v2/users/:userId

Path Parameters
userId (string, Required): The user_id of the user to get.
Response
The user that was retrieved:

created_at (string, Optional)
deleted_at (string, Optional)
email (string, Optional)
fact_rating_instruction (object, Optional)
first_name (string, Optional)
id (integer, Optional)
last_name (string, Optional)
metadata (map from strings to any, Optional)
project_uuid (string, Optional)
session_count (integer, Optional)
updated_at (string, Optional)
user_id (string, Optional)
uuid (string, Optional)
Errors
404: User Get Request Not Found Error
500: User Get Request Internal Server Error
Delete a User
Endpoint
DELETE /api/v2/users/:userId

Path Parameters
userId (string, Required): User ID.
Response
message (string, Optional)
Errors
404: User Delete Request Not Found Error
500: User Delete Request Internal Server Error
Update a User
Endpoint
PATCH /api/v2/users/:userId

Path Parameters
userId (string, Required): User ID.
Request
This endpoint expects an object:

email (string, Optional): The email address of the user.
fact_rating_instruction (object, Optional): Optional instruction to use for fact rating.
first_name (string, Optional): The first name of the user.
last_name (string, Optional): The last name of the user.
metadata (map from strings to any, Optional): The metadata to update.
Response
The user that was updated:

created_at (string, Optional)
deleted_at (string, Optional)
email (string, Optional)
fact_rating_instruction (object, Optional)
first_name (string, Optional)
id (integer, Optional)
last_name (string, Optional)
metadata (map from strings to any, Optional)
project_uuid (string, Optional)
session_count (integer, Optional)
updated_at (string, Optional)
user_id (string, Optional)
uuid (string, Optional)
Errors
400: User Update Request Bad Request Error
404: User Update Request Not Found Error
500: User Update Request Internal Server Error
Get User Facts
Endpoint
GET /api/v2/users/:userId/facts

Path Parameters
userId (string, Required): The user_id of the user to get.
Response
The user facts:

facts (list of objects, Optional)
Errors
404: User Get Facts Request Not Found Error
500: User Get Facts Request Internal Server Error
List All Sessions for a User
Endpoint
GET /api/v2/users/:userId/sessions

Path Parameters
userId (string, Required): User ID.
Response
OK:

classifications (map from strings to strings, Optional)
created_at (string, Optional)
deleted_at (string, Optional)
ended_at (string, Optional)
fact_rating_instruction (object, Optional)
facts (list of strings, Optional)
id (integer, Optional)
metadata (map from strings to any, Optional)
project_uuid (string, Optional)
session_id (string, Optional)
updated_at (string, Optional)
user_id (string, Optional)
uuid (string, Optional)
Errors
500: User Get Sessions Request Internal Server Error
API Reference: User API
Endpoints
Get User Information
GET
https://api.getzep.com/api/v2/users/:userId

Description
Retrieves information about a specific user.

Path Parameters
userId (string, Required): Unique identifier of the user.
Response
200 OK
user_id (string): Unique identifier of the user.
name (string): Name of the user.
email (string): Email address of the user.
created_at (string): Timestamp of when the user was created.
updated_at (string): Timestamp of the last update to the user's information.
Errors
400 Bad Request: Invalid request parameters.
401 Unauthorized: Authentication failed.
404 Not Found: User not found.
500 Internal Server Error: Server encountered an error.
Create New User
POST
https://api.getzep.com/api/v2/users

Description
Creates a new user in the system.

Request
This endpoint expects an object:

name (string, Required): Name of the user.
email (string, Required): Email address of the user.
password (string, Required): Password for the user.
Response
201 Created
user_id (string): Unique identifier of the newly created user.
message (string): Confirmation message.
Errors
400 Bad Request: Invalid input data.
401 Unauthorized: Authentication failed.
500 Internal Server Error: Server encountered an error.
Update User Information
PATCH
https://api.getzep.com/api/v2/users/:userId

Description
Updates information for a specific user.

Path Parameters
userId (string, Required): Unique identifier of the user.
Request
This endpoint expects an object:

name (string, Optional): Updated name of the user.
email (string, Optional): Updated email address of the user.
Response
200 OK
message (string): Confirmation message.
Errors
400 Bad Request: Invalid request parameters.
401 Unauthorized: Authentication failed.
404 Not Found: User not found.
500 Internal Server Error: Server encountered an error.
Delete User
DELETE
https://api.getzep.com/api/v2/users/:userId

Description
Deletes a specific user from the system.

Path Parameters
userId (string, Required): Unique identifier of the user.
Response
200 OK
message (string): Confirmation message.
Errors
400 Bad Request: Invalid request parameters.
401 Unauthorized: Authentication failed.
404 Not Found: User not found.
500 Internal Server Error: Server encountered an error.
# API Reference: User API

*No matching information found for Zep's 'User' API in the provided text.*
# API Reference: Zep 'User' API

## Endpoints

### Get All Edges for a User
**GET** `https://api.getzep.com/api/v2/graph/edge/user/:user_id`

#### Path Parameters
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Required | User ID     |

#### Response
| Field             | Type            | Description                                             |
|-------------------|-----------------|---------------------------------------------------------|
| created_at        | string          | Creation time of the edge                              |
| fact              | string          | Fact representing the edge and nodes that it connects  |
| name              | string          | Name of the edge, relation name                        |
| source_node_uuid  | string          | UUID of the source node                                |
| target_node_uuid  | string          | UUID of the target node                                |
| uuid              | string          | UUID of the edge                                       |
| episodes          | list of strings | (Optional) List of episode ids that reference these entity edges |
| expired_at        | string          | (Optional) Datetime of when the node was invalidated   |
| invalid_at        | string          | (Optional) Datetime of when the fact stopped being true|
| valid_at          | string          | (Optional) Datetime of when the fact became true       |

#### Errors
| Code | Error Description                                    |
|------|-----------------------------------------------------|
| 400  | Edge Get by User ID Request Bad Request Error       |
| 500  | Edge Get by User ID Request Internal Server Error   |

---

### Get All Nodes for a User
**GET** `https://api.getzep.com/api/v2/graph/node/user/:user_id`

#### Path Parameters
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Required | User ID     |

#### Response
| Field             | Type            | Description                           |
|-------------------|-----------------|---------------------------------------|
| created_at        | string          | Creation time of the node            |
| name              | string          | Name of the node                     |
| summary           | string          | Regional summary of surrounding edges|
| uuid              | string          | UUID of the node                     |
| labels            | list of strings | (Optional) Labels associated with the node |

#### Errors
| Code | Error Description                                    |
|------|-----------------------------------------------------|
| 400  | Node Get by User ID Request Bad Request Error       |
| 500  | Node Get by User ID Request Internal Server Error   |

---

### Get Episodes by User ID
**GET** `https://api.getzep.com/api/v2/graph/episodes/user/:user_id`

#### Path Parameters
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| user_id   | string | Required | User ID     |

#### Query Parameters
| Parameter | Type    | Required | Description                                      |
|-----------|---------|----------|--------------------------------------------------|
| lastn     | integer | Optional | The number of most recent episodes to retrieve. |

#### Response
| Field    | Type            | Description |
|----------|-----------------|-------------|
| episodes | list of objects | (Optional)  |

#### Errors
| Code | Error Description                                    |
|------|-----------------------------------------------------|
| 400  | Episode Get by User ID Request Bad Request Error    |
| 500  | Episode Get by User ID Request Internal Server Error|

---
````
