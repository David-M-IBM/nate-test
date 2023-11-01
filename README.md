# aiops-accelerator

- [aiops-accelerator](#aiops-accelerator)
  - [Automation](#automation)
  - [Run the AIOps Accelerator](#run-the-aiops-accelerator)
    - [Automatic (i.e., run containerized)](#automatic-ie-run-containerized)
    - [Manually (i.e., run locally with local dependencies configured)](#manually-ie-run-locally-with-local-dependencies-configured)
  - [Length of Time to Configure](#length-of-time-to-configure)
  - [Architecture](#architecture)
    - [Storage](#storage)
    - [Datastores](#datastores)
  - [Configuration](#configuration)
    - [Datastores](#datastores-1)
      - [Postgres](#postgres)
      - [Kafka](#kafka)
      - [Elasticsearch](#elasticsearch)
      - [Cassandra](#cassandra)
      - [Clickhouse](#clickhouse)
  - [Instana Operator](#instana-operator)
  - [Instana Core](#instana-core)
  - [Instana Unit](#instana-unit)
  - [Instana Agent](#instana-agent)
  - [Troubleshooting](#troubleshooting)
  - [TODO](#todo)
  - [Considerations](#considerations)
  - [Resources](#resources)

## Automation

This end-to-end environment is automated with the following technologies:

Terraform > IBM Cloud > VMWare > OpenShift > Docker > Ansible > AIOps\*

What gets configured is listed below:

```
*AIOPs:
Instana
    - Postgres Datastore
    - Clickhouse Datastore
    - Kafka Datastore
    - Elasticsearch Datastore
    - Cassandra Datastore
    - Instana Operator
    - Instana Core
    - Instana User
    - Instana Unit
    - Instana Routes
    - Instana Agent
    - Instana API Token
    - Instana Website
Turbonomic
    - Turbonomic Operator
    - Kubeturbo
    - Turbonomic Target
    - Turbonomic User
    - Turbonomic Group
    - Turbonomic Policy
Cloud Pak for Watson AIOps (CP4WAIOPS)
    - Foundational Services
    - AI Manager
    - Event Manager
Robot Shop
    - Instana End User Monitoring (EUM)
    - cart Microservice
    - catalogue Microservice
    - dispatch Microservice
    - mongodb Microservice
    - mysql Microservice
    - payment Microservice
    - rabbitmq Microservice
    - ratings Microservice
    - redis Microservice
    - shipping Microservice
    - user Microservice
    - web Microservice
```

## Run the AIOps Accelerator

Reserve a UPI TechZone cluster with the following requirements:

```
OpenShift Version: 4.10 - 4.12
OCS/ODF Size: 5TiB
Worker Node Count: 5
Worker Node Flavor: 32 vCPU x 128 GB - 300 GB ephemeral storage
```
### Automatic (i.e., run containerized)
- Go to the OpenShift Web Console. 
- Add an IBM Entitlement Key to the `pull-secret` secret in the openshift-config namespace.
- Copy and paste the config/aiops-accelerator-deploy.yaml into the OpenShift Web Console. Update the values in the spec.template.spec.containers.args section.
- If you are not providing a value for INSTANA_LICENSE, please remove the line or Instana will have a missing license.

### Manually (i.e., run locally with local dependencies configured)
- Or the following:
- Login to OpenShift.
- Add an IBM Entitlement Key to the `pull-secret` secret in the openshift-config namespace if CONFIGURE_CP4WAIOPS='True'.
- Clone this repository.
- Change directory into the newly cloned GiHub repository.
- Ensure you are on the main branch.
- Provide Instana and Turbonomic secret values in the `group_vars/instana.yaml` and `group_vars/turbonomic.yaml` files
- Copy and paste the config/aiops-accelerator-deploy.yaml into the OpenShift Web Console. Update

  ```
  ansible-playbook aiops-accelerator.yaml
  ```

  NOTE: Run the above command with verbose output by appending the `-vvv` flag to the end of the command.

- Wait until the Ansible Playbook completes. Expected output is the following:

    ```
    PLAY RECAP *******************************************************************************************************************
    localhost                  : ok=147  changed=96   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    
    ```
    
If the Ansible Playbook fails, please open up an issue to provide:
- what was done
- what was expected
- what was the actual outcome
- any output that can prove to be helpful

The issue will be read, reviewed, prioritized and addressed. Thank you.

## Length of Time to Configure

Depends on how long Persistent Volume Claims (PVCs) and Persistent Volumes (PVs) take to configure:

```
Storage: 1 minute
Cert Manager: 1 minute
Postgres: 3 minutes
Clickhouse: 2 minutes (Zookeeper) + 2 minutes (Clickhouse)
Kafka: 2 minutes
Elasticsearch: 2 minutes
Cassandra: 6 minutes
Instana: 1 minute
Core: 20 minutes (Database Migration took 14 minutes)
Unit: 12 minutes (Database Migration took 10 minutes)
Routes: 1 minute
Agent: 1 minute
Robot Shop: 8 minutes
Turbonomic: 7 minutes (User, Group, Policy took 1 minute)
Kubeturbo: 12 minutes (Sending data to Turbonomic took 10 minutes)
```

## Architecture

### Storage

- Datastores require block storage.
- Instana components (e.g., spans-volume-claim, appdata-writer) requires file storage.

### Datastores

- Postgres
- Kafka
- Elasticsearch
- Cassandra
- Clickhouse

## Configuration

### Datastores

#### Postgres

#### Kafka

#### Elasticsearch

#### Cassandra

#### Clickhouse

## Instana Operator

## Instana Core

The Instana Core represents shared components and is responsible for configuring datastore access.

## Instana Unit

## Instana Agent

NOTE: Zookeeper is required as part of the datastores

## Troubleshooting

Wait for Cassandra Operator pod to resolve the following issue:

```
"msg": "Failed to patch object: b'{\"kind\":\"Status\",\"apiVersion\":\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"Internal error occurred: failed calling webhook \\\\\"vcassandradatacenter.kb.io\\\\\": failed to call webhook: Post \\\\\"https://cass-operator-webhook-service.instana-cassandra.svc:443/validate-cassandra-datastax-com-v1beta1-cassandradatacenter?timeout=10s\\\\\": no endpoints available for service \\\\\"cass-operator-webhook-service\\\\\"\",\"reason\":\"InternalError\",\"details\":{\"causes\":[{\"message\":\"failed calling webhook \\\\\"vcassandradatacenter.kb.io\\\\\": failed to call webhook: Post \\\\\"https://cass-operator-webhook-service.instana-cassandra.svc:443/validate-cassandra-datastax-com-v1beta1-cassandradatacenter?timeout=10s\\\\\": no endpoints available for service \\\\\"cass-operator-webhook-service\\\\\"\"}]},\"code\":500}\\n'",
```

Insana Core pods in a CrashLoopBackOff error:
Wait for the spans-volume-claim and appdata-writer PVCs to be Bound to PVs before configuring the Instana Core.

Specify a custom name for the roleBinding:

```
    "msg": "Failure when executing Helm command. Exited 1.\nstdout: Release \"postgres-operator\" does not exist. Installing it now.\n\nstderr: I0601 19:12:41.560590   27341 request.go:601] Waited for 1.072292808s due to client-side throttling, not priority and fairness, request: GET:https://api.ocp-662001vtd7-0bik.cloud.techzone.ibm.com:6443/apis/replication.storage.openshift.io/v1alpha1?timeout=32s\nError: rendered manifests contain a resource that already exists. Unable to continue with install: ClusterRoleBinding \"turbo-all-binding\" in namespace \"\" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key \"app.kubernetes.io/managed-by\": must be set to \"Helm\"; annotation validation error: missing key \"meta.helm.sh/release-name\": must be set to \"postgres-operator\"; annotation validation error: missing key \"meta.helm.sh/release-namespace\": must be set to \"kubeturbo\"\n",
```

Unable to create an Instana user (e.g., a demo user):
Wait (e.g,. 1 minute) before creating an Instana user.

## TODO

Please review all TODO items in this repository's Zenhub. Thank you.

- Configure SSL Certificates for Instana
- Configure a secondary Instana user (e.g., admin)
- Configure Instana as the secondary Instana user
- Configure an Instana Application Perspective
- Configure username and password access to the datastores.
- Instana website tracking
- Configure Turbonomic as the secondary Instana user
- Turbonomic nginxingress: true
- Replace cert-manager deployment with openshift cert-manager operator
- Configure api-token role to be idempotent
- Add imageURL to ConsoleLink resources
- Login to OpenShift with the Ansible kubernetes or openshift module. Then remove the oc dependency in the Dockerfile.
- Configure a secrets manager pod to store secret values.

## Considerations

Consider combining Zookeeper and Clickhouse roles because Zookeeper is configured in the instana-clickhouse namespace along with Clickhouse

## Resources
