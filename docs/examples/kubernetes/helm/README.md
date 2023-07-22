## Getting started with Helm

To deploy `prometheus-api` in Kubernetes, it is easy to use the provided [values.yaml](./values.yaml) file. This will 
deploy the [prometheus-community/prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus)
chart including the `prometheus-api` application as a sidecar container inside the Prometheus pod.

### Get repository info
```shell
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
```

### Install chart
```shell
$ helm install prometheus prometheus-community/prometheus \
--values https://raw.githubusercontent.com/hayk96/prometheus-api/hayk96/main/docs/examples/kubernetes/helm/values.yaml
```

### Verify that everything is working properly
When the chart is installed successfully by executing the following commands, you should see similar output.
```shell
$ kubectl get pod -l app.kubernetes.io/component=server
NAME                                 READY   STATUS    RESTARTS   AGE
prometheus-server-54595bd74b-tr7fb   3/3     Running   0          1m

$ kubectl get svc prometheus-server
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
prometheus-server   ClusterIP   10.100.237.217   <none>        80/TCP    1m

$ kubectl logs -f -l app.kubernetes.io/component=server -c prometheus-api
{"timestamp": "22 Jul 2023 13:13:52", "level": "INFO", "message": "The connection to the Prometheus server has been established successfully!"}
{"timestamp": "22 Jul 2023 13:13:53", "level": "INFO", "message": "Server listening on 0.0.0.0:9090"}
{"timestamp": "22 Jul 2023 13:13:53", "level": "INFO", "message": "-", "status": 200, "method": "POST", "path": "/-/reload"}
{"timestamp": "22 Jul 2023 13:14:09", "level": "INFO", "message": "-", "status": 200, "method": "GET", "path": "/metrics"}
```
Once the apps are ready to handle requests, you can start creating your first Prometheus rules via API.
> **Important:** As you can see, the type of service is `ClusterIP`, which means it's only accessible from within the 
Kubernetes cluster.

### Expose service locally
Port forward the service and open another tab for the next step.
````shell
$ kubectl port-forward svc/prometheus-server 9090:80
````

### Crating example alerting rule via API
> POST /api/v1/rules

**Request**
```shell
curl -i -XPOST 'http://localhost:9090/api/v1/rules' \
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

**Response**
```
HTTP/1.1 201 Created
content-length: 99
content-type: application/json

{"status":"success","message":"The rule was created successfully","file":"scviiavxvnqdpjl.yml"}
```
Where the `scviiavxvnqdpjl.yml` is the randomly generated filename created by the **prometheus-api** server.

### Deleting alerting rule file via API
> DELETE /api/v1/rules/{file}

_Note that the filename in your example is different from the example below._

**Request**
```shell
curl -i -XDELETE 'http://localhost:9090/api/v1/rules/scviiavxvnqdpjl.yml'
```
**Response**
```
HTTP/1.1 204 No Content
content-type: application/json
```
You can find the complete API documentation [here](../../../rest-api). Enjoy!