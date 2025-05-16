# Distributed Key-Value Store

A high-performance, sharded, replicated key-value store implemented in C++ with Raft consensus and a Hack/PHP HTTP API. This project showcases deep infrastructure skills by building core storage components, leader election, replication, and exposing a production-style API.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Building](#building)
   * [Running the Cluster](#running-the-cluster)
5. [HTTP API](#http-api)
6. [Benchmarking](#benchmarking)
7. [Monitoring & Metrics](#monitoring--metrics)
8. [Cluster Management](#cluster-management)
9. [Testing](#testing)
10. [Contributing](#contributing)
11. [License](#license)

---

## Overview

This project implements a distributed, strongly consistent key-value store with the following characteristics:

* **Language:** Core engine in modern C++ (C++17)
* **Consensus:** Raft protocol for leader election and log replication
* **Persistence:** RocksDB for durable storage with an in-memory LRU cache layer
* **Sharding:** Consistent hashing to distribute keys across nodes
* **API Layer:** Hack/PHP HTTP service exposing RESTful endpoints
* **Containerization:** Dockerized components for easy deployment
* **Automation:** Ansible scripts to provision and manage clusters on AWS EC2
* **Monitoring:** Prometheus metrics and Grafana dashboards for observability

## Features

* **Strong consistency** via Raft consensus
* **Horizontal scalability** through sharding
* **High availability** with automatic leader election and failover
* **Persistent storage** backed by RocksDB
* **Low-latency reads/writes** with in-memory caching
* **Simple REST API** for get/put/delete operations
* **Dynamic cluster membership** (add/remove nodes at runtime)
* **Fault injection** support to test resilience under failures

## Architecture

```text
+--------------+      +--------------+      +--------------+
|  KV Node 1   |<---->|  KV Node 2   |<---->|  KV Node 3   |
| (RocksDB +   |  Raft | (RocksDB +   |  Raft | (RocksDB +   |
|  Cache)      | ---->|  Cache)      | ---->|  Cache)      |
+--------------+      +--------------+      +--------------+
       ^                     ^                     ^
       |                     |                     |
       +---------------------------------------------+
                             |
                       Consistent Hash Ring
                             |
                    +------------------------+
                    |   HTTP API Service     |
                    | (Hack/PHP, Dockerized) |
                    +------------------------+
```

* **KV Node**: Each node runs a C++ server implementing Raft, RocksDB storage, and an in-memory cache.
* **API Service**: Stateless Hack/PHP container that routes requests to the current Raft leader.
* **Cluster Management**: Ansible playbooks to spin up the desired number of nodes and configure networking.

## Getting Started

### Prerequisites

* **Compiler:** GCC or Clang with C++17 support
* **Libraries:** RocksDB, libuv, OpenSSL
* **Docker & Docker Compose** (v1.28+)
* **Ansible** (v2.9+)

### Building

```bash
# Clone the repo
git clone https://github.com/YourUsername/distributed-kv-store.git
cd distributed-kv-store

# Build core C++ server
mkdir build && cd build
cmake ..
make -j4

# Build HTTP API Docker image
cd ../api
docker build -t kv-api:latest .
```

### Running the Cluster

```bash
# Spin up 3-node cluster locally with Docker Compose
docker-compose up -d

# Verify nodes are up
docker-compose ps

# Initialize the cluster (assign IDs and start Raft)
docker exec -it kv-node1 ./bin/kvserver --init --id 1 --peers kv-node2:5000,kv-node3:5000
docker exec -it kv-node2 ./bin/kvserver --init --id 2 --peers kv-node1:5000,kv-node3:5000
docker exec -it kv-node3 ./bin/kvserver --init --id 3 --peers kv-node1:5000,kv-node2:5000
```

## HTTP API

| Method | Endpoint    | Description             |
| ------ | ----------- | ----------------------- |
| GET    | `/kv/{key}` | Retrieve value by key   |
| PUT    | `/kv/{key}` | Store or update a value |
| DELETE | `/kv/{key}` | Remove a key-value pair |

Example with `curl`:

```bash
# Write
curl -X PUT http://localhost:8080/kv/user123 -d '"{"name":"Alice"}"'

# Read
curl http://localhost:8080/kv/user123

# Delete
curl -X DELETE http://localhost:8080/kv/user123
```

## Benchmarking

A simple Go-based tool (`benchmark/bench.go`) generates load and measures latency:

```bash
# Build benchmark tool
cd benchmark
go build -o bench

# Run 10k ops/sec for 60 seconds against kv-node1
./bench --addr localhost:8080 --ops 10000 --duration 60s
```

Metrics collected:

* **Throughput** (ops/sec)
* **P50, P90, P99 latency**
* **Error rates** under leader failover

## Monitoring & Metrics

* Prometheus config in `monitoring/prometheus.yml`
* Grafana dashboards in `monitoring/grafana/`

Key metrics:

* `raft_leader_changes_total`
* `kv_requests_total`
* `kv_request_duration_seconds`
* `rocksdb_compactions`
* `cache_hit_rate`

## Cluster Management

Ansible playbook (`ansible/site.yml`) provisions EC2 instances, installs dependencies, and configures Docker Compose:

```bash
cd ansible
ansible-playbook -i hosts site.yml
```

Use `hosts` inventory to define your cluster nodes and variables.

## Testing

* **Unit tests** in `tests/` using Google Test framework. Run:

  ```bash
  cd build
  ctest --output-on-failure
  ```
* **Integration tests** simulate network partitions and leader failover scenarios.

## Contributing

Contributions are welcome! Please open issues for bugs or feature requests, fork the repo, and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
