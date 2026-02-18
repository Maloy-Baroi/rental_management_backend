# API Documentation with drf-spectacular (Swagger)

## Overview

This project uses **drf-spectacular** to provide interactive API documentation through Swagger UI and ReDoc. The documentation is auto-generated from your Django REST Framework views and serializers.

## Accessing the Documentation

Once your development server is running, you can access the API documentation at:

### Swagger UI (Interactive)
- **URL**: http://localhost:8000/api/docs/
- **Features**: 
  - Interactive API exploration
  - Test API endpoints directly from the browser
  - See request/response examples
  - Authentication support

### ReDoc (Read-only)
- **Features**: 
  - Clean, three-panel design
  - Searchable documentation
  - Better for reading and understanding APIs

### OpenAPI Schema (Raw)
- **URL**: http://localhost:8000/api/schema/
- **Format**: YAML/JSON
- **Use**: Import into Postman, Insomnia, or other API clients

## Configuration

### Settings (config/settings.py)

The following settings are configured for drf-spectacular:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Rental Management API',
    'DESCRIPTION': 'Production-grade rental/property management system API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # Offline Swagger UI
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',  # Offline ReDoc
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'SECURITY': [{'bearerAuth': []}],
    'COMPONENTS': {
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
}
```

### REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # ... other settings
}
```

## Using Authentication in Swagger UI

1. **Get Access Token**: 
   - Use the `/api/v1/auth/login/` endpoint to get your JWT token
   - Or use `/api/v1/auth/register/` to create a new account first

2. **Authorize in Swagger**:
   - Click the **"Authorize"** button (🔒) at the top right of Swagger UI
   - Enter your token as: `Bearer YOUR_ACCESS_TOKEN`
   - Click "Authorize"
   - Now all authenticated endpoints will include your token

## Generating Static Schema File

To generate a static OpenAPI schema file:

```bash
python manage.py spectacular --color --file schema.yml
```

This generates a `schema.yml` file that can be:
- Committed to version control
- Used for API versioning
- Imported into API testing tools
- Shared with frontend developers

## Customizing Documentation

### Adding Descriptions to ViewSets

```python
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        description="List all properties",
        summary="Get properties list",
        tags=['Properties']
    ),
    retrieve=extend_schema(
        description="Get a specific property by ID",
        summary="Get property detail",
        tags=['Properties']
    ),
)
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
```

### Adding Custom Parameters

```python
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='status',
            type=OpenApiTypes.STR,
            description='Filter by status',
            enum=['active', 'inactive', 'pending']
        ),
    ]
)
def list(self, request):
    # Your implementation
    pass
```

### Adding Response Examples

```python
from drf_spectacular.utils import OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Property Example',
            value={
                'id': 1,
                'name': 'Luxury Apartment',
                'address': '123 Main St',
                'status': 'active'
            },
            response_only=True,
        ),
    ]
)
def retrieve(self, request, pk=None):
    # Your implementation
    pass
```

## API Tags

The following tags are configured for organizing endpoints:

- **Authentication**: User authentication and registration
- **Properties**: Property, unit, and location management
- **Contracts**: Rental contract management
- **Billing**: Bill generation and management
- **Payments**: Payment processing and tracking
- **Audit**: Audit log and system tracking

## Available Endpoints

### Authentication (`/api/v1/auth/`)
- `POST /register/` - Register new user
- `POST /login/` - Login and get JWT token
- `POST /logout/` - Logout user
- `POST /token/refresh/` - Refresh JWT token
- `GET /profile/` - Get user profile
- `PUT /profile/` - Update user profile

### Properties (`/api/v1/properties/`)
- Property management endpoints
- Unit management endpoints
- Location management endpoints

### Contracts (`/api/v1/contracts/`)
- Contract creation and management
- Contract status updates

### Billing (`/api/v1/billing/`)
- Bill generation
- Bill management and tracking

### Payments (`/api/v1/payments/`)
- Payment processing
- Payment history

### Audit (`/api/v1/audit/`)
- Audit log retrieval
- System activity tracking

## Best Practices

1. **Keep Documentation Updated**: Use docstrings and `@extend_schema` decorators
2. **Test Endpoints**: Use Swagger UI to test your APIs during development
3. **Version Control**: Commit generated schema.yml for tracking API changes
4. **Security**: Never expose real credentials in examples
5. **Clear Descriptions**: Write clear, concise descriptions for all endpoints

## Troubleshooting

### Swagger UI Not Loading
- Check that `drf-spectacular` and `drf-spectacular-sidecar` are installed
- Verify `DEFAULT_SCHEMA_CLASS` is set in REST_FRAMEWORK settings
- Ensure URLs are properly configured in `config/urls.py`

### Missing Endpoints
- Check that your views/viewsets are properly registered in URLs
- Verify that permission classes aren't blocking the schema generation
- Run `python manage.py spectacular --validate` to check for issues

### Authentication Not Working
- Ensure you're using the format: `Bearer YOUR_TOKEN`
- Check that your token hasn't expired
- Verify JWT settings in `SIMPLE_JWT` configuration

## Additional Resources

- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

## Development Workflow

1. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

2. **Access Swagger UI**:
   Open http://localhost:8000/api/docs/

3. **Test Endpoints**:
   - Register/Login to get a token
   - Authorize using the token
   - Test all endpoints interactively

4. **Generate Schema** (Optional):
   ```bash
   python manage.py spectacular --file schema.yml
   ```

## Production Considerations

- The sidecar mode ensures Swagger UI works offline (no CDN dependencies)
- Schema generation is cached for performance
- Consider disabling Swagger UI in production or protecting it with authentication
- Use the static schema file for client generation or API contracts

