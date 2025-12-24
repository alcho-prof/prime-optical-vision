# Cloud Storage Configuration Guide

## Overview
This guide explains how to configure cloud storage for production deployment.

---

## Option 1: AWS S3 (Recommended)

### Prerequisites
1. AWS Account
2. S3 Bucket created
3. IAM User with S3 access

### Step 1: Install Required Packages

```bash
pip install boto3 django-storages
```

Add to `requirements.txt`:
```
boto3==1.35.76
django-storages==1.14.4
```

### Step 2: Update Settings

Add to `config/settings/production.py`:

```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'prime-optical-media')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')  # Mumbai
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1 day
}
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False

# Static files (CSS, JS)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files (uploaded images)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

### Step 3: Environment Variables

Add to `.env`:
```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_STORAGE_BUCKET_NAME=prime-optical-media
AWS_S3_REGION_NAME=ap-south-1
```

### Step 4: Create S3 Bucket

1. Go to AWS Console → S3
2. Click "Create bucket"
3. Bucket name: `prime-optical-media`
4. Region: `ap-south-1` (Mumbai) or nearest to your users
5. Uncheck "Block all public access"
6. Create bucket

### Step 5: Set Bucket Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::prime-optical-media/*"
        }
    ]
}
```

### Step 6: Create IAM User

1. Go to IAM → Users → Create user
2. Username: `prime-optical-app`
3. Attach policy: `AmazonS3FullAccess`
4. Create access key
5. Copy Access Key ID and Secret Access Key to `.env`

---

## Option 2: DigitalOcean Spaces (Simpler)

### Step 1: Install Package

```bash
pip install boto3 django-storages
```

### Step 2: Create Space

1. Go to DigitalOcean → Spaces
2. Create Space: `prime-optical`
3. Region: `blr1` (Bangalore)
4. CDN: Enable

### Step 3: Configuration

```python
# DigitalOcean Spaces (S3-compatible)
AWS_ACCESS_KEY_ID = os.environ.get('DO_SPACES_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('DO_SPACES_SECRET')
AWS_STORAGE_BUCKET_NAME = 'prime-optical'
AWS_S3_ENDPOINT_URL = 'https://blr1.digitaloceanspaces.com'
AWS_S3_REGION_NAME = 'blr1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.blr1.cdn.digitaloceanspaces.com'
AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

**Cost:** $5/month for 250GB + 1TB transfer

---

## Option 3: Cloudinary (Image-Specific)

### Step 1: Install

```bash
pip install cloudinary django-cloudinary-storage
```

### Step 2: Configuration

```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

**Benefits:**
- Auto image optimization
- Automatic resizing
- Image transformations
- CDN included

**Cost:** Free tier: 25GB storage, 25GB bandwidth/month

---

## Client Upload Process

### Via Django Admin (No Code Changes Needed)

1. Client logs into admin: `https://primeoptical.in/admin/`
2. Goes to Products → Add Product
3. Adds product variant
4. Clicks "Choose File" → Selects frame image
5. Clicks "Save"

**What Happens:**
- Image uploaded to browser
- Django receives image
- **If local storage:** Saved to `media/products/variants/`
- **If S3:** Uploaded to S3 bucket automatically
- **If Cloudinary:** Uploaded and optimized automatically
- Path saved in MySQL database
- Image accessible via URL

### Example URLs:

**Local Storage:**
```
https://primeoptical.in/media/products/variants/aviator-gold.jpg
```

**AWS S3:**
```
https://prime-optical-media.s3.ap-south-1.amazonaws.com/media/products/variants/aviator-gold.jpg
```

**Cloudinary:**
```
https://res.cloudinary.com/prime-optical/image/upload/v1/media/products/variants/aviator-gold.jpg
```

---

## Migration from Local to Cloud

If you start with local storage and want to migrate later:

```bash
# Install AWS CLI
pip install awscli

# Sync local media to S3
aws s3 sync backend/media/ s3://prime-optical-media/media/ --acl public-read

# Update settings to use S3
# Images now served from S3
```

---

## Recommended Setup for Your Client

### Development (Your Machine):
- Local storage (`backend/media/`)
- Fast, no costs
- Easy debugging

### Staging (Test Server):
- DigitalOcean Spaces or S3
- Test cloud storage
- Similar to production

### Production (Client's Server):
- **AWS S3** (if high traffic, global users)
- **DigitalOcean Spaces** (if simpler, India-focused)
- **Cloudinary** (if image optimization important)

---

## Cost Estimation

### Scenario: 1000 products, 3 images each, 500KB average

**Storage:** 1000 × 3 × 0.5MB = 1.5GB
**Bandwidth:** 10,000 views/month × 0.5MB = 5GB/month

#### AWS S3:
- Storage: 1.5GB × $0.023 = $0.03/month
- Bandwidth: 5GB × $0.09 = $0.45/month
- **Total: ~$0.50/month**

#### DigitalOcean Spaces:
- **Flat: $5/month** (includes 250GB storage + 1TB transfer)

#### Cloudinary:
- **Free tier** (if under 25GB storage + 25GB bandwidth)
- Otherwise: $89/month (includes optimization)

---

## What to Tell Your Client

### Option A: Budget-Conscious
"We'll use DigitalOcean Spaces for $5/month. You upload images through the admin panel, and they're automatically stored in the cloud with CDN for fast loading worldwide."

### Option B: Enterprise
"We'll use AWS S3 with CloudFront CDN. Costs about $10-20/month depending on traffic. Industry standard, highly reliable, used by Netflix, Airbnb, etc."

### Option C: Image-Heavy
"We'll use Cloudinary. It automatically optimizes images, creates thumbnails, and serves them fast. Free for small sites, $89/month for larger catalogs."

---

## Implementation Checklist

- [ ] Choose cloud storage provider
- [ ] Create account and bucket/space
- [ ] Install required packages
- [ ] Update production settings
- [ ] Add credentials to `.env`
- [ ] Test upload in staging
- [ ] Migrate existing images (if any)
- [ ] Update documentation for client
- [ ] Train client on admin panel

---

**Recommendation:** Start with **DigitalOcean Spaces** - simple, affordable, India-based servers.
