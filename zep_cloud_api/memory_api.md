# Memory API

## Classify a session (cloud only)

### POST

`https://api.getzep.com/api/v2/sessions/:sessionId/classify`

### Description

Classify a session by session id.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Request

This endpoint expects an object.

- **classes** (list of strings, Required): The classes to use for classification.
- **name** (string, Required): The name of the classifier. Will be used to store the classification in session metadata if persist is True.
- **instruction** (string, Optional): Custom instruction to use for classification.
- **last_n** (integer, Optional, Defaults to 4): The number of session messages to consider for classification. Defaults to 4.
- **persist** (boolean, Optional): Whether to persist the classification to session metadata. Defaults to True.

### Response

A response object containing the following:

- **class** (string, Optional)
- **label** (string, Optional)

### Errors

- **404**: Memory Classify Session Request Not Found Error
- **500**: Memory Classify Session Request Internal Server Error

---

## End a session (cloud only)

### POST

`https://api.getzep.com/api/v2/sessions/:sessionId/end`

### Description

End a session by ID.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Request

This endpoint expects an object.

- **classify** (object, Optional)

### Response

- **OK**

Additional fields:

- **classification** (object, Optional)
- **session** (object, Optional)

### Errors

- **400**: Memory End Session Request Bad Request Error
- **404**: Memory End Session Request Not Found Error
- **500**: Memory End Session Request Internal Server Error

---

## Returns all facts for a session by ID (cloud only)

### GET

`https://api.getzep.com/api/v2/sessions/:sessionId/facts`

### Description

Get facts for a session.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Query Parameters

- **minRating** (double, Optional): Minimum rating by which to filter facts (Zep Cloud only)

### Response

The facts for the session.

- **facts** (list of objects, Optional)

### Errors

- **404**: Memory Get Session Facts Request Not Found Error
- **500**: Memory Get Session Facts Request Internal Server Error

---

## Adds facts to a session (cloud only)

### POST

`https://api.getzep.com/api/v2/sessions/:sessionId/facts`

### Description

Adds facts to a session.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Request

This endpoint expects an object.

- **facts** (list of objects, Optional)

### Response

- **OK**

Additional fields:

- **message** (string, Optional)

### Errors

- **404**: Memory Add Session Facts Request Not Found Error
- **500**: Memory Add Session Facts Request Internal Server Error

---

## Get session memory

### GET

`https://api.getzep.com/api/v2/sessions/:sessionId/memory`

### Description

Returns a memory (latest summary, list of messages and facts) for a given session.

### Path Parameters

- **sessionId** (string, Required): The ID of the session for which to retrieve memory.

### Query Parameters

- **lastn** (integer, Optional): The number of most recent memory entries to retrieve.
- **minRating** (double, Optional): The minimum rating by which to filter facts.

### Response

- **OK**

Fields:

- **context** (string, Optional): Memory context containing relevant facts and entities for the session. Can be put into the prompt directly.
- **facts** (list of strings, Optional): Most recent list of facts derived from the session. (cloud only)
- **messages** (list of objects, Optional): A list of message objects, where each message contains a role and content. Only last_n messages will be returned.
- **metadata** (map from strings to any, Optional): A dictionary containing metadata associated with the memory.
- **relevant_facts** (list of objects, Optional): Most relevant facts to the recent messages in the session.
- **summary** (object, Optional): The most recent summary before last nth message. (cloud only)

### Errors

- **404**: Memory Get Request Not Found Error
- **500**: Memory Get Request Internal Server Error

---

## Add memory to the specified session.

### POST

`https://api.getzep.com/api/v2/sessions/:sessionId/memory`

### Description

Add memory to the specified session.

### Path Parameters

- **sessionId** (string, Required): The ID of the session to which memory should be added.

### Request

This endpoint expects an object.

- **messages** (list of objects, Required): A list of message objects, where each message contains a role and content.
- **fact_instruction** (string, Optional): Additional instruction for generating the facts. Zep Cloud Only, will be ignored on Community Edition.
- **return_context** (boolean, Optional): Optionally return memory context relevant to the most recent messages.
- **summary_instruction** (string, Optional): Additional instruction for generating the summary. Zep Cloud Only, will be ignored on Community Edition.

### Response

An object, optionally containing memory context retrieved for the last message.

- **context** (string, Optional)

### Errors

- **500**: Memory Add Request Internal Server Error

---

## Delete memory messages for a given session

### DELETE

`https://api.getzep.com/api/v2/sessions/:sessionId/memory`

### Description

Delete memory messages by session ID.

### Path Parameters

- **sessionId** (string, Required): The ID of the session for which memory should be deleted.

### Response

- **OK**

## Lists messages for a session

**GET** `https://api.getzep.com/api/v2/sessions/:sessionId/messages`

Lists messages for a session, specified by limit and cursor.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Query Parameters

- **limit** (integer, Optional): Limit the number of results returned
- **cursor** (integer, Optional): Cursor for pagination

### Response

- **OK**
  - **messages** (list of objects, Optional): A list of message objects.
  - **row_count** (integer, Optional): The number of messages returned.
  - **total_count** (integer, Optional): The total number of messages.

### Errors

- **404**: Memory Get Session Messages Request Not Found Error
- **500**: Memory Get Session Messages Request Internal Server Error

---

## Gets a specific message from a session

**GET** `https://api.getzep.com/api/v2/sessions/:sessionId/messages/:messageUUID`

Gets a specific message from a session.

### Path Parameters

- **sessionId** (string, Required): The ID of the session.
- **messageUUID** (string, Required): The UUID of the message.

### Response

- **The message.**
  - **content** (string): The content of the message.
  - **role_type** (enum): The type of the role (e.g., “user”, “system”).
  - **created_at** (string, Optional): The timestamp of when the message was created.
  - **metadata** (map from strings to any, Optional): The metadata associated with the message.
  - **role** (string, Optional): The role of the sender of the message (e.g., “user”, “assistant”).
  - **token_count** (integer, Optional): The number of tokens in the message.
  - **updated_at** (string, Optional): The timestamp of when the message was last updated.
  - **uuid** (string, Optional): The unique identifier of the message.

### Errors

- **404**: Memory Get Session Message Request Not Found Error
- **500**: Memory Get Session Message Request Internal Server Error

---

## Updates the metadata of a message

**PATCH** `https://api.getzep.com/api/v2/sessions/:sessionId/messages/:messageUUID`

Updates the metadata of a message.

### Path Parameters

- **sessionId** (string, Required): The ID of the session.
- **messageUUID** (string, Required): The UUID of the message.

### Request

- **metadata** (map from strings to any, Required): The metadata to update.

### Response

- **The updated message.**
  - **content** (string): The content of the message.
  - **role_type** (enum): The type of the role (e.g., “user”, “system”).
  - **created_at** (string, Optional): The timestamp of when the message was created.
  - **metadata** (map from strings to any, Optional): The metadata associated with the message.
  - **role** (string, Optional): The role of the sender of the message (e.g., “user”, “assistant”).
  - **token_count** (integer, Optional): The number of tokens in the message.
  - **updated_at** (string, Optional): The timestamp of when the message was last updated.
  - **uuid** (string, Optional): The unique identifier of the message.

### Errors

- **404**: Memory Update Message Metadata Request Not Found Error
- **500**: Memory Update Message Metadata Request Internal Server Error

---

## Search memory for the specified session (cloud only) [Deprecated]

**POST** `https://api.getzep.com/api/v2/sessions/:sessionId/search`

Search memory for the specified session. Deprecated, please use `search_sessions` method instead.

### Path Parameters

- **sessionId** (string, Required): The ID of the session for which memory should be searched.

### Query Parameters

- **limit** (integer, Optional): The maximum number of search results to return. Defaults to None (no limit).

### Request

- **metadata** (map from strings to any, Optional): Metadata Filter
- **min_fact_rating** (double, Optional)
- **min_score** (double, Optional)
- **mmr_lambda** (double, Optional)
- **search_scope** (enum, Optional): Allowed values: `messages`, `summary`, `facts`
- **search_type** ("similarity" or "mmr", Optional): Allowed values: `similarity`, `mmr`
- **text** (string, Optional)

### Response

- A list of SearchResult objects representing the search results.
  - **message** (object, Optional)
    - **metadata** (map from strings to any, Optional)
    - **score** (double, Optional)
  - **summary** (object, Optional)

### Errors

- **404**: Memory Search Request Not Found Error
- **500**: Memory Search Request Internal Server Error

---

## Returns a session's summaries by ID (cloud only) [Deprecated]

**GET** `https://api.getzep.com/api/v2/sessions/:sessionId/summary`

Get session summaries by ID.

### Path Parameters

- **sessionId** (string, Required): Session ID

### Response

- **OK**
  - **row_count** (integer, Optional)
  - **summaries** (list of objects, Optional)
  - **total_count** (integer, Optional)

### Errors

- **404**: Memory Get Summaries Request Not Found Error
- **500**: Memory Get Summaries Request Internal Server Error

---

## Synthesize a question (cloud only)

**GET** `https://api.getzep.com/api/v2/sessions/:sessionId/synthesize_question`

Synthesize a question from the last N messages in the chat history.

### Path Parameters

- **sessionId** (string, Required): The ID of the session.

### Query Parameters

- **lastNMessages** (integer, Optional): The number of messages to use for question synthesis.

### Response

- **The synthesized question.**
  - **question** (string, Optional)

### Errors

- **404**: Memory Synthesize Question Request Not Found Error
- **500**: Memory Synthesize Question Request Internal Server Error

---
