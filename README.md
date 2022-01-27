![CI Status](https://github.com/sogno-platform/cim-service/actions/workflows/ci.yml/badge.svg)

# CIM Service

This is a server which provides an [OpenAPI](http://spec.openapis.org/oas/v3.0.3) REST API for [CIMpy](https://git.rwth-aachen.de/acs/public/cim/cimpy).
This can be used to upload and process grid data specified by the IEC61970 standard.

The server is based on [connexion](https://github.com/zalando/connexion) which itself builds upon [flask](https://flask.palletsprojects.com/en/1.1.x/).
The API is specified in the [openapi.yaml](openapi.yaml).

## Requirements

- Python 3.5.2+
- CIMpy python packages and dependencies specified by [requirements.txt](./requirements.txt). Install them with `pip3 install -r requirements.txt`

## Usage

### To run the server directly, please execute the following from the root directory:

```bash
python3 server.py
```

### To run in docker:

```bash
docker run --name=redis-master redis
docker build -t cim-service .
docker run --name cim-service -p 8080:8080 cim-service
```

To access the OpenAPI UI, open http://localhost:8080/ui in your browser.

### To run in Kubernetes:

This will become easier when we have uploaded the docker containers to docker hub.

#### Install redis
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis
```

#### Install docker registry
```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

#### Install cim-service
```bash
docker build -t cim-service .
docker tag cim-service:latest localhost:5000/cim-service:latest
docker push localhost:5000/cim-service
helm install cim-service helm/ --values helm/values.yaml
```

To access the OpenAPI UI, print the local URL and then open it in your browser:
```bash
export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services cim-service)
export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT
```

## Development:

Notes for developers:

- The repository contains set of vscode configurations at (.vscode)[.vscode/]

### Code Structure

The [server.py](./server.py) invokes the connexion server with the _openapi.yaml_ as argument. The connexion server then parses the yaml and provides the general server functionality.
The developer then has to provide the callbacks to the service which should be called by the API.
The name of the callback function is specified in the _openapi.yaml_ as `operationID` (example: `operationId: cimadapter.get_models`).
The basic job is then to provide these callbacks.

The convention for the ANM4L server is to put the callbacks into the project root with a name like `XYZadapter.py`.

The _openapi-generator_ also generates a set of classes which correspond to the `schema` from the openapi.yaml.
These can be used to ease the parsing of requests and the generation of responses.
All of these classes are located at [models](./models/).

### Code Generation/API Changes

The fundamental code structure is generated with the [OpenAPITool openapi-generator]( https://github.com/OpenAPITools/openapi-generator).
If the openapi.yaml has changed, you can run the [generate_api_code.sh](generate_api_code.sh) script to generate these files again.

**However, these files must be adapted manually!** The quality of the generated code is not sufficient.
Examples of what must be adapted:

- _openapi-generator_ puts all the server files into a folder `openapi`, which is this an unnecessary hierarchy.
You need to copy the generated files to the corresponding folder in the repository **and** fix the `import` lines in the python code.
- _openapi-generator_ generates some useless files. Not all "models" are needed for the implementation
- _openapi-generator_ creates sometimes unnecessary imports. Characteristic examples: `connexion`, `six`, `json`. Also sometimes files are imported twice.

**Recommended approach:**

Generate the files and then use a diff editor such as [meld](https://meldmerge.org) to selectively import the changed code. Example:

```bash
meld generated/openapi_server/models models
```

### Testing

This project uses `pytest` for integration tests. All integration test can be found in [test](test/). To invoke it manually call:

```bash
pytest  -cov test/
```

(pytest should easily integrate into your IDE...)
