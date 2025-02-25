# Hashly-
Here’s how I built  Hashly, a terminal-based hash lookup tool, from scratch.  
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### **1. `terminal-based`**  

## **Step 1: Connect to Your EC2 Instance**  
```bash
ssh -i yourkey.pem username@<ip-address>
```
- Replace `yourkey.pem` with your private key.
- 
- Pro tip: Use `-v` for debugging connection issues.  

---

## **Step 2: Install Dependencies** 

### Update System Packages  
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Essentials  
```bash
sudo apt install -y git python3 python3-pip python3-venv docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

---

## **Step 3: Set Up Hashly**  

### Create a Python Virtual Environment  
```bash
python3 -m venv env
source env/bin/activate
```

### Install Dependencies  
```bash
pip install typesense==0.14.0
```

---

## **Step 4: Run Typesense (Search Engine)**  

### Pull Docker Image  
```bash
docker pull typesense/typesense:0.24.1
```

### Start Container  
```bash
docker run -d -p 8108:8108 -v ~/typesense-data:/data \
typesense/typesense:0.24.1 \
--data-dir /data --api-key "$(openssl rand -hex 32)"
```

### Verify It’s Running  
```bash
curl http://localhost:8108/health  # Should return {"ok":true}
```

---

## **Step 5: Import Hashes & Run the Tool**  
```bash
python3 import_hashes.py  # Populate your dataset
python3 search_hash.py    # Start searching!
```

---

## **Why This Works**  
- **Docker**: Isolates the search engine for easy management.  
- **Virtual Environment**: Avoids dependency conflicts.  
- **Terminal-First Design**: Perfect for scripting and automation.  
