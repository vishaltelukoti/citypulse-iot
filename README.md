# CityPulse – IoT Sensor Aggregation Mesh (PoC)

CityPulse is a **production-style Python capstone project** that demonstrates advanced Python concepts by simulating an IoT sensor aggregation platform.

It showcases **metaclasses, design patterns, asyncio concurrency, NumPy vectorization, memory management, security best practices, testing, profiling, and containerized deployment**.


##  Features

###  Architecture (Part 1)

* Metaclass-based auto-registration of sensors
* Abstract Base Classes (ABC)
* Design Patterns:

  * Factory (`DeviceFactory`)
  * Singleton (`GridConfig`)
  * Observer (`EmergencyResponseSystem`)
  * Strategy (`WiFiStrategy`, `LoRaWanStrategy`)

###  Concurrency (Part 2)

* Async ingestion using `asyncio.gather()`
* Non-blocking simulated sensor polling
* Generator-based streaming

###  Performance (Part 3)

* Vectorized calculations with **NumPy** (no Python loops for math)
* Memory management using `WeakValueDictionary`
* Explicit garbage collection demo
* Benchmark comparing Python loops vs NumPy

###  Security (Part 4)

* SHA-256 hashing
* Fernet encryption/decryption
* Safe file path handling
* SQL injection-safe queries using parameterized SQL

###  Quality

* Type hints throughout
* PEP 8–style code
* Modular package structure
* Unit tests with `unittest`
* Profiling using `cProfile` and `tracemalloc`

###  Deployment

* Multi-stage **Dockerfile**
* Kubernetes **Deployment** and **HPA (Horizontal Pod Autoscaler)**
* Reproducible builds


##  Project Structure

```
CityPulse_IoT/
├── main.py
├── profiling.py
├── requirements.txt
├── README.md
├── analytics/
├── core/
├── sensors/
├── ingestion/
├── security/
├── tests/
│   ├── __init__.py
│   └── test_suite.py
├── var/
│   └── logs/
└── deployment/
    ├── Dockerfile
    ├── deployment.yaml
    └── hpa.yaml
```


##  Requirements

* Python **3.10+** (recommended: 3.11)
* Docker Desktop
* (Optional) Minikube / Kubernetes

### Install Python dependencies

```bash
pip install -r requirements.txt
```

Dependencies:

* numpy
* pandas
* cryptography

(Everything else used is from the Python standard library.)


##  Running Locally (Without Docker)

From the project root:

```bash
python main.py
```

You should see output demonstrating:

* Architecture patterns
* Security features
* Performance & memory management
* Async ingestion


##  Running Tests

From the project root:

```bash
python -m unittest tests.test_suite
```


##  Profiling

Run CPU + memory profiling:

```bash
python profiling.py
```

This will show:

* CPU hotspots (via `cProfile`)
* Peak memory usage (via `tracemalloc`)


##  Docker Deployment (Multi-stage Build)

`Dockerfile` is inside the `deployment/` folder, so we must reference it explicitly.

### Build the image

From the **project root**:

```bash
docker build -t citypulse:latest -f deployment/Dockerfile .
```

### Run the container

```bash
docker run --rm citypulse:latest
```

You should see the same output as `python main.py`.


##  Kubernetes Deployment (Minikube)

### 1. Start Minikube

```bash
minikube start
```

### 2. Load image into Minikube

```bash
minikube image load citypulse:latest
```

### 3. Apply manifests

```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/hpa.yaml
```

### 4. Check status

```bash
kubectl get pods
kubectl get hpa
```

### 5. View logs

```bash
kubectl logs -l app=citypulse
```


##  Autoscaling (HPA)

The `hpa.yaml` is configured to:

* Scale from **2 pods -> 10 pods**
* When CPU usage exceeds **70%**


##  Purpose of This PoC

This project demonstrates:

* Advanced Python architecture
* Async concurrency with `asyncio`
* High-performance computing with NumPy
* Memory safety and garbage collection
* Secure coding practices
* Testing and profiling
* Containerized and Kubernetes-based deployment


## Author

**Vishal**

*Capstone Project:* **CityPulse – IoT Sensor Aggregation Mesh**
