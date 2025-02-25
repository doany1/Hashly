## 🔒Part 2 – How I Gave My Project a HTTPS Makeover (For Free)  

---

## **Why I Ditched Terminal-Only Mode**  
1. **Browsers are bullies**: Chrome throws “Not Secure” warnings for HTTP.  
2. **IP addresses are ugly**: `http://54.203.22.1:5000` looks like a robot’s Social Security number.  
3. **Let’s Encrypt exists**: Free SSL certificates? Yes, please.  

---

## **Tools You’ll Need**  
- An AWS EC2 instance   
- 15 minutes of patience  
- A DuckDNS account (free)  

---

## **Step 1: Claim Your Free DuckDNS Domain**  
### (Or: “How I Tricked the Internet into Thinking I Owned a Domain”)  

1. Go to [DuckDNS.org](https://www.duckdns.org).  
2. Sign in with GitHub (no new passwords!).  
3. Claim a subdomain like `hashly-tool.duckdns.org`.
   
4. **Note your token** (it’s on the DuckDNS dashboard).  

---

## **Step 2: Automate IP Updates**  
### (Or: “Teaching a Duck to Track My EC2 IP”)  

EC2 instances get new IPs when restarted. DuckDNS needs to know your latest IP.  

### Create a DuckDNS Updater Script  
```bash  
mkdir -p ~/scripts && nano ~/scripts/duckdns.sh  
```  

Paste this (replace `YOUR_SUBDOMAIN` and `YOUR_TOKEN`):  
```bash  
#!/bin/bash  
curl -s "https://www.duckdns.org/update?domains=YOUR_SUBDOMAIN&token=YOUR_TOKEN&ip="  
```  

### Make It Executable  
```bash  
chmod +x ~/scripts/duckdns.sh  
```  

### Schedule It to Run Every 5 Minutes  
```bash  
(crontab -l ; echo "*/5 * * * * ~/scripts/duckdns.sh >/dev/null 2>&1") | crontab -  
```  

**Test it:**  
```bash  
~/scripts/duckdns.sh  # Should return "OK"  
```  

---

## **Step 3: Install Nginx & Certbot**  
### (Or: “Nginx: The Bouncer of the Internet”)  

Nginx will act as a reverse proxy. Certbot will handle SSL certificates.  

```bash  
sudo apt update  
sudo apt install nginx certbot python3-certbot-nginx -y  
```  

---

## **Step 4: Configure Nginx**  
### (Or: “YAML Files Are My Sleep Paralysis Demon”)  

### Create an Nginx Config File  
```bash  
sudo nano /etc/nginx/sites-available/hashly  
```  

Paste this (replace `your-subdomain.duckdns.org`):  
```nginx  
server {  
    listen 80;  
    server_name your-subdomain.duckdns.org;  

    location / {  
        proxy_pass http://localhost:5000;  # Forward to Flask  
        proxy_set_header Host $host;  
        proxy_set_header X-Real-IP $remote_addr;  
    }  
}  
```  

### Enable the Config

```bash  
sudo ln -s /etc/nginx/sites-available/hashly /etc/nginx/sites-enabled/  
sudo rm /etc/nginx/sites-enabled/default  # Delete the default "Welcome to Nginx" page  
sudo systemctl restart nginx  
```  

**Check for errors:**  
```bash  
sudo nginx -t  # Should say "syntax is okay"  
```  

---

## **Step 5: Get Your Free SSL Certificate**  
### (Or: “Certbot: The Robot Santa of HTTPS”)  

Run Certbot to automate SSL setup:  
```bash  
sudo certbot --nginx -d your-subdomain.duckdns.org --email your@email.com --agree-tos --non-interactive  
```  

Certbot will:  
1. Generate SSL certificates.  
2. Modify your Nginx config to force HTTPS.  
3. Set up auto-renewal (certificates expire every 90 days).  

**Verify auto-renewal:**  
```bash  
sudo certbot renew --dry-run  
```  

---

## **Step 6: Lock Down Flask**  
### (Or: “Don’t Let the Internet Yell at Your Python App”)  

Modify your Flask app (`app.py`) to **only listen locally**:  
```python  
if __name__ == '__main__':  
    app.run(host='127.0.0.1', port=5000)  # No direct internet access!  
```  

**Restart Flask:**  
```bash  
pkill -f "python3 app.py"  # Kill old instances  
python3 app.py &           # Run in background  
```  

---

## **Step 7: Open EC2 Security Group Ports**  
### (Or: “AWS Security Groups: The Digital Bouncer”)  

1. Go to **AWS EC2 Console > Security Groups**.  
2. Edit inbound rules to allow:  
   - **HTTP (Port 80)**  
   - **HTTPS (Port 443)**  

---

## **Step 8: Test Your HTTPS Setup**  
Visit `https://your-subdomain.duckdns.org`.  

**Success looks like:**  
✅ Padlock icon in the browser’s address bar.  
✅ No warnings about “insecure connections.”  

---

## **Common Facepalm Moments (And Fixes)**  

### 1. **“Nginx Won’t Restart!”**  
**Fix:** Check for typos in your config:  
```bash  
sudo nginx -t  # Points you to the line causing trouble  
```  

### 2. **“Certbot Fails with ‘Connection Refused’”**  
**Fix:** Did you open ports 80/443 in AWS?  

### 3. **“My DuckDNS Domain Shows an Old IP”**  
**Fix:** Run the updater script manually:  
```bash  
~/scripts/duckdns.sh  
```  

---

## **Why This Setup Rocks**  
1. **Free Forever**: No domain fees, no SSL costs.  
2. **Auto-Renewing Certificates**: Certbot handles it.  
3. **Looks Professional**:  `https://hashly.duckdns.org/` 

---


This completes the journey from terminal tool to secure web app—all while keeping your wallet closed. 🚀
