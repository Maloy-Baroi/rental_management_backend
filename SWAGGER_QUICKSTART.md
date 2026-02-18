# Swagger Setup Complete - Quick Start Guide

## ✅ What Was Fixed

### 1. **Redis Connection Error Fixed**
**Problem**: Throttling was trying to use Redis cache, causing 500 errors when Redis wasn't running.

**Solution**: Disabled default throttling in REST_FRAMEWORK settings. Throttling can be enabled per-view when Redis is available.

```python
# In config/settings.py
REST_FRAMEWORK = {
    # ... other settings ...
    # Throttling disabled by default - enable per-view when Redis is available
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
}
```

### 2. **Schema Endpoints Made Public**
**Problem**: Schema/Swagger endpoints required authentication by default.

**Solution**: 
- Added `permission_classes=[]` to all schema views in URLs
- Added `SERVE_PERMISSIONS`: `['rest_framework.permissions.AllowAny']` to SPECTACULAR_SETTINGS

```python
# In config/urls.py
path('api/schema/', SpectacularAPIView.as_view(permission_classes=[]), name='schema'),
path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[]), name='swagger-ui'),
# ... etc
```

## 🚀 How to Use

### 1. Start Your Server
```bash
cd /home/maloy-baroi/Downloads/SystemJudge/dream/backend/rental_management_backend/rental_management_backend
python manage.py runserver
```

### 2. Access Swagger UI
Open your browser and go to:
- **Primary**: http://localhost:8000/api/schema/swagger-ui/
- **Alternative**: http://localhost:8000/api/docs/

### 3. Access ReDoc
- **Primary**: http://localhost:8000/api/schema/redoc/
- **Alternative**: http://localhost:8000/api/redoc/

### 4. Get OpenAPI Schema
- **JSON/YAML**: http://localhost:8000/api/schema/

## 📋 Available Endpoints

All your API endpoints will be automatically documented:

- **Authentication** (`/api/v1/auth/`)
  - Register, Login, Logout, Profile, Token Refresh

- **Properties** (`/api/v1/properties/`)
  - Property, Unit, Location management

- **Contracts** (`/api/v1/contracts/`)
  - Rental contract management

- **Billing** (`/api/v1/billing/`)
  - Bill generation and management

- **Payments** (`/api/v1/payments/`)
  - Payment processing

- **Audit** (`/api/v1/audit/`)
  - Audit logs

## 🔑 Testing with Authentication

1. **Get JWT Token**:
   - Go to `/api/v1/auth/login/` endpoint in Swagger
   - Click "Try it out"
   - Enter credentials and execute
   - Copy the `access` token from response

2. **Authorize**:
   - Click the **"Authorize"** button (🔒) at top-right
   - Enter: `Bearer YOUR_ACCESS_TOKEN`
   - Click "Authorize"
   - Close the dialog

3. **Test Protected Endpoints**:
   - Now all authenticated endpoints will work
   - The token will be automatically included in requests

## 🛠️ Configuration Summary

### Files Modified

1. **config/settings.py**
   - Disabled default throttling (commented out)
   - Added `SERVE_PERMISSIONS` to SPECTACULAR_SETTINGS
   - Kept all other Spectacular settings intact

2. **config/urls.py**
   - Added `permission_classes=[]` to all schema views
   - Configured multiple URL paths for flexibility

### Dependencies (Already Installed)

```
drf-spectacular==0.27.0
drf-spectacular-sidecar==2024.1.1
```

## ⚠️ Important Notes

### Redis Not Required for Swagger
- Swagger/documentation works WITHOUT Redis
- Redis is only needed if you enable throttling

### Re-enabling Throttling (Optional)
If you want to enable throttling later (when Redis is running):

```python
# In config/settings.py
REST_FRAMEWORK = {
    # ... other settings ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}
```

### Making Schema Private (Production)
For production, you may want to protect the schema:

```python
# In config/urls.py
from rest_framework.permissions import IsAuthenticated

path('api/schema/', SpectacularAPIView.as_view(permission_classes=[IsAuthenticated]), name='schema'),
```

## 🎯 Next Steps

1. ✅ Start your server: `python manage.py runserver`
2. ✅ Open Swagger: http://localhost:8000/api/schema/swagger-ui/
3. ✅ Test your endpoints interactively
4. ✅ Share the API docs with your frontend team

## 📚 Additional Documentation

- Full guide: See `API_DOCUMENTATION.md`
- Setup summary: See `SWAGGER_SETUP_SUMMARY.md`

---

**Status**: ✅ **WORKING - Swagger is now fully functional!**

**Last Updated**: February 18, 2026

