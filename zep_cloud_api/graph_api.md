# Zep Graph API Reference

## Add Data to Graph

### POST `/api/v2/graph`

#### Request

This endpoint expects an object.

- **data**
  - **list of objects**  
    Required  
    The data to be added to the graph.

#### Response

The added data.

- **message**
  - **string**  
    Optional

#### Errors

- **400**  
  Graph Add Data Request Bad Request Error
- **500**  
  Graph Add Data Request Internal Server Error

---

## Search Graph

### POST `/api/v2/graph/search`

#### Request

This endpoint expects an object.

- **query**
  - **object**  
    Required  
    The search query object.

#### Response

Search results from the graph.

- **results**
  - **list of objects**  
    Optional

#### Errors

- **400**  
  Graph Search Request Bad Request Error
- **404**  
  Graph Search Request Not Found Error
- **500**  
  Graph Search Request Internal Server Error

## TODO: INCOMPLETE
