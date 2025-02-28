## 🌐💻 Part 1 – How I Built My Cybersecurity Project from Scratch



It was 2 AM. The coffee had gone cold, and my terminal blinked back at me like a smug owl. *“Build a hash lookup tool,”* I’d told myself earlier that day. *“How hard could it be?”*  

Turns out, pretty hard. But after a week of Googling, swearing at SSH keys, and befriending Docker errors, **Hashly** was born—a terminal-powered tool to hunt down suspicious file hashes. Here’s *exactly* how I did it.  

---

## The Tools You’ll Need  
- An AWS EC2 free tier instance (Ubuntu)  
---

## Step 1: Connect to Your EC2 Instance  
### (Or: “Why Is SSH So Fussy?”)  

I stared at the AWS console, copied my instance’s public IP, and typed:  
```bash  
ssh -i ~/Downloads/my-key.pem ubuntu@<your-ec2-ip>  
```  

What went wrong:  
- Permission denied? Fixed with:  
  ```bash  
  chmod 400 ~/Downloads/my-key.pem   
  ```  
  **“Connection timed out”**? Check your EC2 security group—it needs inbound SSH access (port 22).  

---

## Step 2: Install the Essentials 
### (Or: “sudo apt install patience”)  

First rule of Linux: *update everything*.  

```bash  
sudo apt update && sudo apt upgrade -y   
```  

Then, the toolkit:  
```bash  
sudo apt install -y git python3 python3-pip python3-venv docker.io  
```  

**Why these packages?**  
- **Git**: To clone my future GitHub repo (or rescue code from accidental `rm -rf` disasters).  
- **Python3 + pip**: Because Python is the duct tape of cybersecurity tools.  
- **Docker**: To containerize the search engine (Typesense) and avoid dependency hell.  

*Don’t forget to start Docker:*  
```bash  
sudo systemctl start docker  
sudo systemctl enable docker   
```  

---

## **Step 3: Create a Python Virtual Environment**  
### (Or: “Isolation Is Good, Actually”)  

Python dependencies can clash like toddlers in a sandbox. Virtual environments save the day:  

```bash  
python3 -m venv env 
source env/bin/activate    
```  

*Now install the critical library:*  
```bash  
pip install typesense==0.14.0 
```  



---

## **Step 4: Deploy Typesense with Docker**  
### (Or: “Containers Are Magic Tupperware”)  

**Typesense** is the search engine that powers Hashly. Here’s how I tamed it:  

### Pull the Docker Image  
```bash  
docker pull typesense/typesense:0.24.1  
```  

### Generate an API Key (Like a Boss)  
```bash  
openssl rand -hex 32  # Copy this output. Treat it like a password.  
```  

### Launch the Container  
```bash  
docker run -d \  
  -p 8108:8108 \  
  -v ~/typesense-data:/data \  
  typesense/typesense:0.24.1 \  
  --data-dir /data \  
  --api-key "your-generated-api-key-here"  
```  

**Breakdown:**  
- `-d`: Detached mode (runs in the background).  
- `-v ~/typesense-data:/data`: Saves data to your EC2 instance (so it survives container restarts).  
- `--api-key`: Use the key from `openssl rand`.  

### Verify It’s Alive  
```bash  
curl http://localhost:8108/health  
```  
If you see `{"ok":true}`, pop the (non-alcoholic) champagne.  

---

## **Step 5: Import Hashes & Run the Tool**  
### (Or: “The Moment of Truth”)  

### Import Your Hash Dataset  
Assuming you have a `hash.txt` file. if you don't have read this 
```bash  
python3 import_hashes.py    
```  

### Search for a Hash  
```bash  
python3 search_hash.py  
```  
*Then type a hash like `5d41402abc4b2a76b9719d911017c592` and hit Enter.*  

If it returns a match (or a “Not found”), you’ve just built a cybersecurity tool.  

---

## **Common Fire-Drills (And How I Survived Them)**  

### 1. **“Docker Permission Denied”**  
**Fix:** Add your user to the `docker` group:  
```bash  
sudo usermod -aG docker $USER  
newgrp docker  # Reload group permissions  
```  

### 2. **“Typesense Won’t Start”**  
**Check the logs:**  
```bash  
docker logs <container-id>  # Find the ID with `docker ps`  
```  

### 3. **“Python Can’t Find typesense”**  
**Did you activate the virtual environment?**  
```bash  
source env/bin/activate    
```  

---

## **Why This Setup Rocks**  
1. **Terminal-Only**: No GUIs, no distractions.  
2. **Dockerized Search Engine**: Isolated, portable, and easy to update.  
  

---

## **What’s Next?**  
In [Part 2](https://github.com/doany1/Hashly-/blob/c6c2df18d3c2336408990d02d7a55f5b408a4ddd/Part2/Guide.md), I’ll show you how to:  
- Turn this terminal tool into a secure web app  
- Get a free domain with HTTPS (no credit card required)  

