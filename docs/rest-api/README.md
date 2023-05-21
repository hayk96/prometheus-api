# Rules API v1

This documentation is for the Rules API, where you can find comprehensive information and instructions on how to use it.  

<details>
 <summary>
    <b>POST</b> <code><b>/api/v1/rules</b></code>
</summary>

The operation creates a new rule file with a randomly generated filename. It requires a JSON request body and returns a 
successful response if the requested body is valid, matches the required schema, and has a correct Prometheus query expression. The generated filename is then returned in the response.

#### Parameters

`None`

#### Request body

`Content-Type: application/json`

#### Responses

  - Success
    ```
    HTTP/1.1  201 Created
    Content-Type: application/json
 
    {
      "status": "success",
      "file": "example-rule.yml",
      "message": "The rule was created successfully"
    }
    ```

  - Error
    ```
    HTTP/1.1  422 Unprocessable Entity
    Content-Type: application/json
        
    {
      "detail": [
        {
          "loc": [
            "body"
          ],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```
    ```
    HTTP/1.1  500
    Content-Type: application/json
 
    {
      "status": "error",
      "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
    }
    ```    

#### Example cURL

```shell
curl -i -XPOST 'http://localhost:5000/api/v1/rules' \
--header 'Content-Type: application/json' \
--data '{
  "data": {
    "groups": [
      {
        "name": "ServiceHealthAlerts",
        "rules": [
          {
            "alert": "HighCPUUsage",
            "expr": "sum(rate(cpu_usage{job=\"webserver\"}[5m])) > 0.8",
            "for": "5m",
            "labels": {
              "severity": "warning"
            },
            "annotations": {
              "summary": "High CPU Usage Detected",
              "description": "The CPU usage for the web server is {{ $value }}% for the last 5 minutes."
            }
          }
        ]
      }
    ]
  }
}'
```
</details>


<details>
 <summary>
    <b>PUT</b> <code><b>/api/v1/rules/{file}</b></code>
</summary>

The operation takes a rule filename as a request parameter and requires a JSON request body. It returns a successful 
response if the requested body is valid, matches the required schema, and has a correct Prometheus query expression.
#### Parameters

`file` - required

#### Request body

`Content-Type: application/json`

#### Responses

  - Success
    ```
    HTTP/1.1  201 Created
    Content-Type: application/json
 
    {
      "status": "success",
      "message": "The rule was created successfully"
    }
    ```

  - Error
    ```
    HTTP/1.1  409 Conflict
    Content-Type: application/json
      
    {
      "status": "error",
      "message": "The requested file already exists"
    }
    ```
    ```
    HTTP/1.1  422 Unprocessable Entity
    Content-Type: application/json
        
    {
      "detail": [
        {
          "loc": [
            "body"
          ],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```
    ```
    HTTP/1.1  500 Internal Server Error
    Content-Type: application/json
 
    {
      "status": "error",
      "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
    }
    ```   

#### Example cURL

```shell
curl -i -XPUT 'http://localhost:5000/api/v1/rules/example-rule.yml' \
--header 'Content-Type: application/json' \
--data '{
  "data": {
    "groups": [
      {
        "name": "ServiceHealthAlerts",
        "rules": [
          {
            "alert": "HighCPUUsage",
            "expr": "sum(rate(cpu_usage{job=\"webserver\"}[5m])) > 0.8",
            "for": "5m",
            "labels": {
              "severity": "warning"
            },
            "annotations": {
              "summary": "High CPU Usage Detected",
              "description": "The CPU usage for the web server is {{ $value }}% for the last 5 minutes."
            }
          }
        ]
      }
    ]
  }
}'
```
</details>



<details>
 <summary>
    <b>DELETE</b> <code><b>/api/v1/rules/{file}</b></code>
</summary>

Creates new rule file with the name of requested parameter.
#### Parameters

`file` - required

#### Request body

`None`

#### Responses

  - Success
    ```
    HTTP/1.1  204 No Content
    Content-Type: application/json
    ```

  - Error
    ```
    HTTP/1.1  404 Not Found
    Content-Type: application/json
      
    {
      "status": "error",
      "message": "File not found"
    }
    ```
    ```
    HTTP/1.1  500 Internal Server Error
    Content-Type: application/json
 
    {
      "status": "error",
      "message": "failed to reload config: one or more errors occurred while applying the new configuration (--config.file=\"/etc/prometheus/prometheus.yml\")\n"
    }
    ```   

#### Example cURL
The operation takes a rule filename as a request parameter and does not require a request body. It returns a successful 
response if the rule filename exists.

```shell
curl -i -XDELETE -H 'Content-Type: application/json' 'http://localhost:5000/api/v1/rules/example-rule.yml'
```
</details>