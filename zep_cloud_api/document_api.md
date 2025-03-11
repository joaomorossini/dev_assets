# Document API

## Deletes a DocumentCollection (Deprecated)

### Endpoint

**DELETE**  
`https://api.getzep.com/api/v2/collections/:collectionName`

### Description

If a collection with the same name already exists, it will be overwritten.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Response

| Field     | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `message` | string | No       |             |

### Errors

| Code | Description                                              |
| ---- | -------------------------------------------------------- |
| 400  | Document Delete Collection Request Bad Request Error     |
| 401  | Document Delete Collection Request Unauthorized Error    |
| 404  | Document Delete Collection Request Not Found Error       |
| 500  | Document Delete Collection Request Internal Server Error |

---

## Updates a DocumentCollection (Deprecated)

### Endpoint

**PATCH**  
`https://api.getzep.com/api/v2/collections/:collectionName`

### Description

Updates a DocumentCollection.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Request

This endpoint expects an object.

| Field         | Type   | Required | Description       |
| ------------- | ------ | -------- | ----------------- |
| `description` | string | No       | <=1000 characters |
| `metadata`    | map    | No       |                   |

### Response

| Field     | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `message` | string | No       |             |

### Errors

| Code | Description                                              |
| ---- | -------------------------------------------------------- |
| 400  | Document Update Collection Request Bad Request Error     |
| 401  | Document Update Collection Request Unauthorized Error    |
| 404  | Document Update Collection Request Not Found Error       |
| 500  | Document Update Collection Request Internal Server Error |

---

## Creates Multiple Documents in a DocumentCollection (cloud only, Deprecated)

### Endpoint

**POST**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents`

### Description

Creates Documents in a specified DocumentCollection and returns their UUIDs.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Request

This endpoint expects a list of objects.

| Field         | Type   | Required | Description      |
| ------------- | ------ | -------- | ---------------- |
| `content`     | string | Yes      |                  |
| `document_id` | string | No       | <=100 characters |
| `metadata`    | map    | No       |                  |

### Response

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |

### Errors

| Code | Description                                          |
| ---- | ---------------------------------------------------- |
| 400  | Document Add Documents Request Bad Request Error     |
| 401  | Document Add Documents Request Unauthorized Error    |
| 500  | Document Add Documents Request Internal Server Error |

---

## Batch Deletes Documents from a DocumentCollection by UUID (cloud only, Deprecated)

### Endpoint

**POST**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/batchDelete`

### Description

Deletes specified Documents from a DocumentCollection.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Request

This endpoint expects a list of strings.

### Response

| Field     | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `message` | string | No       |             |

### Errors

| Code | Description                                                   |
| ---- | ------------------------------------------------------------- |
| 400  | Document Batch Delete Documents Request Bad Request Error     |
| 401  | Document Batch Delete Documents Request Unauthorized Error    |
| 500  | Document Batch Delete Documents Request Internal Server Error |

---

## Batch Gets Documents from a DocumentCollection (cloud only, Deprecated)

### Endpoint

**POST**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/batchGet`

### Description

Returns Documents from a DocumentCollection specified by UUID or ID.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Request

This endpoint expects an object.

| Field          | Type            | Required | Description |
| -------------- | --------------- | -------- | ----------- |
| `document_ids` | list of strings | No       |             |
| `uuids`        | list of strings | No       |             |

### Response

| Field         | Type            | Required | Description |
| ------------- | --------------- | -------- | ----------- |
| `content`     | string          | No       |             |
| `created_at`  | string          | No       |             |
| `document_id` | string          | No       |             |
| `embedding`   | list of doubles | No       |             |
| `is_embedded` | boolean         | No       |             |
| `metadata`    | map             | No       |             |
| `updated_at`  | string          | No       |             |
| `uuid`        | string          | No       |             |

### Errors

| Code | Description                                                |
| ---- | ---------------------------------------------------------- |
| 400  | Document Batch Get Documents Request Bad Request Error     |
| 401  | Document Batch Get Documents Request Unauthorized Error    |
| 500  | Document Batch Get Documents Request Internal Server Error |

---

## Batch Updates Documents in a DocumentCollection (cloud only, Deprecated)

### Endpoint

**PATCH**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/batchUpdate`

### Description

Updates Documents in a specified DocumentCollection.

### Path Parameters

| Parameter        | Type   | Required | Description                     |
| ---------------- | ------ | -------- | ------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection |

### Request

This endpoint expects a list of objects.

| Field         | Type   | Required | Description     |
| ------------- | ------ | -------- | --------------- |
| `uuid`        | string | Yes      |                 |
| `document_id` | string | No       | <=40 characters |
| `metadata`    | map    | No       |                 |

### Response

| Field     | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `message` | string | No       |             |

### Errors

| Code | Description                                                   |
| ---- | ------------------------------------------------------------- |
| 400  | Document Batch Update Documents Request Bad Request Error     |
| 401  | Document Batch Update Documents Request Unauthorized Error    |
| 500  | Document Batch Update Documents Request Internal Server Error |

---

## Gets a Document from a DocumentCollection by UUID (cloud only, Deprecated)

### Endpoint

**GET**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/uuid/:documentUUID`

### Description

Returns specified Document from a DocumentCollection.

### Path Parameters

| Parameter        | Type   | Required | Description                        |
| ---------------- | ------ | -------- | ---------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection    |
| `documentUUID`   | string | Yes      | UUID of the Document to be updated |

### Response

| Field         | Type            | Required | Description |
| ------------- | --------------- | -------- | ----------- |
| `content`     | string          | No       |             |
| `created_at`  | string          | No       |             |
| `document_id` | string          | No       |             |
| `embedding`   | list of doubles | No       |             |
| `is_embedded` | boolean         | No       |             |
| `metadata`    | map             | No       |             |
| `updated_at`  | string          | No       |             |
| `uuid`        | string          | No       |             |

### Errors

| Code | Description                                                                                |
| ---- | ------------------------------------------------------------------------------------------ |
| 400  | Get Collections Collection Name Documents Uuid Document Uuid Request Bad Request Error     |
| 401  | Get Collections Collection Name Documents Uuid Document Uuid Request Unauthorized Error    |
| 500  | Get Collections Collection Name Documents Uuid Document Uuid Request Internal Server Error |

---

## Delete Document from a DocumentCollection by UUID (cloud only, Deprecated)

### Endpoint

**DELETE**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/uuid/:documentUUID`

### Description

Delete specified Document from a DocumentCollection.

### Path Parameters

| Parameter        | Type   | Required | Description                        |
| ---------------- | ------ | -------- | ---------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection    |
| `documentUUID`   | string | Yes      | UUID of the Document to be deleted |

### Response

| Field     | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `message` | string | No       |             |

### Errors

| Code | Description                                            |
| ---- | ------------------------------------------------------ |
| 400  | Document Delete Document Request Bad Request Error     |
| 401  | Document Delete Document Request Unauthorized Error    |
| 404  | Document Delete Document Request Not Found Error       |
| 500  | Document Delete Document Request Internal Server Error |

---

## Updates a Document (cloud only, Deprecated)

### Endpoint

**PATCH**  
`https://api.getzep.com/api/v2/collections/:collectionName/documents/uuid/:documentUUID`

### Description

Updates a Document in a DocumentCollection by UUID.

### Path Parameters

| Parameter        | Type   | Required | Description                        |
| ---------------- | ------ | -------- | ---------------------------------- |
| `collectionName` | string | Yes      | Name of the Document Collection    |
| `documentUUID`   | string | Yes      | UUID of the Document to be updated |
