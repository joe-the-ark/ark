# Deployment Guide: Adding safecircles.ch Domain

This guide will help you set up both `arks.ch` and `safecircles.ch` domains to serve the same Django application.

## Prerequisites

- Both domains must point to your server's IP address in DNS
- Nginx is installed and running
- Let's Encrypt (certbot) is installed
- Django application is running on port 8888

## Step-by-Step Instructions

### Step 1: Update DNS Records

Ensure both domains have A records pointing to your server's IP:

```
arks.ch           → Your Server IP
www.arks.ch       → Your Server IP
safecircles.ch    → Your Server IP
www.safecircles.ch → Your Server IP
```

Wait for DNS propagation (can take a few minutes to 48 hours). Verify with:
```bash
dig arks.ch
dig safecircles.ch
```

### Step 2: Update SSL Certificate

You need to include `safecircles.ch` in your SSL certificate. Run:

```bash
# Stop nginx temporarily
sudo systemctl stop nginx

# Obtain or renew certificate with all domains
sudo certbot certonly --standalone -d arks.ch -d www.arks.ch -d safecircles.ch -d www.safecircles.ch

# Or if renewing an existing certificate:
sudo certbot certonly --standalone --expand -d arks.ch -d www.arks.ch -d safecircles.ch -d www.safecircles.ch
```

**Note:** The certificate will be stored at `/etc/letsencrypt/live/arks.ch/` (or you may need to specify a different path if certbot creates a new certificate).

### Step 3: Update Nginx Configuration

The `ark2020.nginx` file has already been updated to include both domains. Review it to ensure it's correct:

```bash
cat ark2020.nginx
```

### Step 4: Deploy Nginx Configuration

Run the deployment script:

```bash
chmod +x nginx_script.sh
sudo ./nginx_script.sh
```

Or manually:

```bash
sudo cp ark2020.nginx /etc/nginx/sites-available/
sudo rm -f /etc/nginx/sites-enabled/ark2020.nginx
sudo ln -s /etc/nginx/sites-available/ark2020.nginx /etc/nginx/sites-enabled/
```

### Step 5: Test Nginx Configuration

```bash
sudo nginx -t
```

You should see:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Step 6: Restart Nginx

```bash
sudo systemctl restart nginx
# Or
sudo service nginx restart
```

### Step 7: Verify Django Settings

The `backend/backend/settings_prod.py` file has been updated with `ALLOWED_HOSTS` including both domains. Verify:

```python
ALLOWED_HOSTS = ['127.0.0.1', '192.168.3.103', '10.192.12.148', 'arks.ch', 'www.arks.ch', 'safecircles.ch', 'www.safecircles.ch']
```

### Step 8: Restart Django Application

Restart your Django application (however you're running it - gunicorn, supervisor, etc.):

```bash
# If using supervisor:
sudo supervisorctl restart ark2020

# Or if using systemd:
sudo systemctl restart your-django-service

# Or if using gunicorn directly:
# (find the process and restart)
```

### Step 9: Test Both Domains

Test that both domains work:

```bash
curl -I https://arks.ch
curl -I https://www.arks.ch
curl -I https://safecircles.ch
curl -I https://www.safecircles.ch
```

All should return `200 OK` or `302` redirects.

### Step 10: Set Up Auto-Renewal for SSL

Ensure certbot auto-renewal is working:

```bash
sudo certbot renew --dry-run
```

If successful, add to crontab (usually already done by certbot):
```bash
sudo crontab -l
# Should show something like:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## Troubleshooting

### SSL Certificate Issues

If certbot fails with "connection refused" or "timeout", ensure:
- DNS is properly configured
- Port 80 is accessible from the internet
- No firewall is blocking Let's Encrypt

### Nginx 502 Bad Gateway

- Check if Django is running: `ps aux | grep gunicorn`
- Check Django logs
- Verify Django is listening on `127.0.0.1:8888`

### Domain Not Resolving

- Check DNS with: `dig your-domain.ch`
- Wait for DNS propagation (up to 48 hours)
- Clear DNS cache: `sudo systemd-resolve --flush-caches`

### Mixed Content Warnings

Ensure all resources (CSS, JS, images) use HTTPS or relative URLs.

## Verification Checklist

- [ ] DNS records point to server IP
- [ ] SSL certificate includes all 4 domains
- [ ] Nginx configuration is updated and tested
- [ ] Django ALLOWED_HOSTS includes all domains
- [ ] Django application is running and accessible
- [ ] Both domains serve identical content
- [ ] HTTP redirects to HTTPS work
- [ ] SSL certificate auto-renewal is configured

## Additional Notes

- Both domains will serve the exact same Django application
- Sessions and data will be shared between domains
- If you need domain-specific behavior later, you can use `request.get_host()` in Django views
- SSL certificates expire after 90 days - certbot should auto-renew them

