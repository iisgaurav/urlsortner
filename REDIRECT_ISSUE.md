# REDIRECT WORKAROUND GUIDE

## Problem
Render only exposes port 10000 (Streamlit). Django redirects are on port 8000 (internal).
Short URLs like `https://urlsortner-l65b.onrender.com/abc123` don't work because Streamlit can't handle custom paths.

## Solution Options:

### Option 1: Use Query Parameter Format (Quick Fix)
Update SHORT_URL_DOMAIN to use query parameters:
```
SHORT_URL_DOMAIN=https://urlsortner-l65b.onrender.com/?r=
```

Then modify Django to accept `/?r=abc123` format.

### Option 2: Deploy Django Separately (Recommended)
Deploy Django API as a separate service on Render:
1. Create another Render web service for Django only
2. Set Django SHORT_URL_DOMAIN to Django service URL
3. Keep Streamlit UI separate

This way:
- Django: `https://urlsortner-api.onrender.com/abc123` → redirects work
- Streamlit: `https://urlsortner-ui.onrender.com` → UI works

### Option 3: Use Nginx Reverse Proxy (Advanced)
Add Nginx to route:
- `/api/*` → Django (port 8000)
- `/{short_code}` → Django (port 8000)  
- `/` → Streamlit (port 10000)

This requires Docker Compose with Nginx service.

## Quick Test
For now, share links in this format:
`https://urlsortner-l65b.onrender.com` and manually enter short code in Analytics tab.

## Recommended Next Step
Deploy Django separately on Render for proper redirect functionality.
