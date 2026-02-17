# Professional Admin Panel Setup

## Overview
All models have been registered in the Django Admin panel with a beautiful, professional design using **Django Jazzmin**. The admin interface now includes:

- 🎨 Modern, Bootstrap-based UI
- 📊 Advanced filtering and search capabilities
- 🔍 Inline editing for related models
- 📈 Statistics and summaries on list pages
- 🎯 Custom actions for bulk operations
- 🎨 Color-coded status badges
- 📱 Responsive design
- 🔐 Permission-based access control

## Registered Models

### 1. Accounts App (`apps/accounts/admin.py`)
- **User**: Custom user model with phone-based authentication
  - Status badges (Active/Inactive/Deleted)
  - Bulk actions: Activate, Deactivate, Soft Delete
  - Advanced filtering by status, role, and creation date
  
- **Household**: Tenant/household information
  - Personal information management
  - NID validation
  - Associated user tracking

### 2. Properties App (`apps/properties/admin.py`)
- **Location**: Geographic location management
  - Hierarchical address structure
  - Search by area, district, division
  
- **Property**: Building/property information
  - Amenity badges (Lift, Security, Parking, Tiled)
  - Photo management (JSON)
  - Inline unit management
  
- **Unit**: Individual apartments/units
  - Availability badge (Available/Occupied)
  - Inline editing for:
    - Room summary
    - Rental terms
    - Unit policies
    - Utilities
  - Smart property relationship
  
- **UnitRoomSummary**: Room configuration
  - Bedrooms, bathrooms, kitchens, balconies
  - Master bedroom tracking
  
- **RentalTerms**: Rental pricing and terms
  - Asking and minimum rent
  - Advance payment months
  - Service charges
  - Payment due day
  
- **UnitPolicy**: Unit-specific rules
  - Pet policy
  - Bachelor/gender restrictions
  - Sublet permissions
  - AC installation rights
  
- **UtilityType**: Utility categories
  - Electricity, Water, Gas, Internet, etc.
  
- **UnitUtility**: Unit-specific utilities
  - Billing type (Meter/Card/Fixed)
  - Rent inclusion status

### 3. Contracts App (`apps/contracts/admin.py`)
- **RentalContract**: Lease agreements
  - Status badges (Active/Terminated/Expired)
  - Contract duration calculator
  - Inline participants and authors
  - Bulk actions: Terminate, Mark as Expired
  - Financial terms tracking
  
- **RentalContractParticipant**: Contract members
  - Primary tenant and dependents
  - Role management
  
- **RentalContractAuthor**: Contract managers
  - Permission levels (Approve, Terminate, Renew)
  - Active status management
  - Bulk activate/deactivate actions

### 4. Billing App (`apps/billing/admin.py`)
- **Bill**: Rent and utility bills
  - Status badges (Pending/Paid/Overdue/Partial)
  - Payment progress bars
  - Automatic overdue detection
  - Summary statistics:
    - Total bills and amount
    - Paid bills count
    - Overdue bills count
  - Bulk actions: Mark as Paid, Overdue, Pending
  - Date hierarchy navigation

### 5. Payments App (`apps/payments/admin.py`)
- **Payment**: Payment transactions
  - Status badges (Pending/Processing/Succeeded/Failed/Refunded)
  - Provider tracking (Stripe, Cash, Bank Transfer, Mobile Money)
  - Summary statistics:
    - Total payments and amount
    - Success/failure rates
    - By provider breakdown
  - Bulk actions: Mark as Succeeded, Failed, Refunded
  
- **PaymentWebhook**: Webhook events
  - Processing status badges
  - Provider and event type tracking
  - Error message logging
  - Bulk actions: Mark as Processed, Retry Processing
  - Summary statistics by provider and event type

### 6. Audit App (`apps/audit/admin.py`)
- **AuditLog**: System audit trail
  - Action badges (Create/Update/Delete/Approve/etc.)
  - Formatted JSON data display
  - Content object links
  - IP address and user agent tracking
  - Read-only (no add/delete permissions)
  - Summary statistics:
    - Total logs
    - By action type
    - By entity type
    - Top actors

## Admin Panel Features

### 🎨 Visual Design
- **Color-coded badges**: Easy status identification
- **Progress bars**: Visual payment tracking
- **Icons**: Font Awesome icons for each model
- **Clean layout**: Professional Bootstrap theme
- **Dark sidebar**: Modern, easy-on-eyes design

### 🔍 Search & Filter
- **Advanced search**: Full-text search across relevant fields
- **Smart filters**: Pre-configured filters for common queries
- **Date hierarchy**: Easy navigation by date
- **Related field search**: Search through foreign key relationships

### ⚡ Performance Optimizations
- **Select related**: Optimized queries with `select_related()`
- **Prefetch related**: Efficient loading of related objects
- **Pagination**: 25-50 items per page
- **Autocomplete**: Fast foreign key selection

### 🛠️ Bulk Actions
- **User management**: Activate, deactivate, soft delete
- **Contract management**: Terminate, mark as expired
- **Bill management**: Mark as paid, overdue, pending
- **Payment management**: Update status in bulk
- **Webhook management**: Retry processing, mark as processed

### 📊 Statistics & Summaries
- **Real-time counts**: Total records, filtered counts
- **Aggregated data**: Sum totals, averages
- **Grouped statistics**: By status, provider, type
- **Top performers**: Most active users, top amounts

### 📱 Responsive Design
- **Mobile-friendly**: Works on tablets and phones
- **Fixed sidebar**: Easy navigation
- **Collapsible sections**: Clean form layouts
- **Inline editing**: Edit related objects without leaving page

## Configuration

### Jazzmin Settings (in `config/settings.py`)

```python
JAZZMIN_SETTINGS = {
    "site_title": "Rental Management",
    "site_header": "Rental Management System",
    "site_brand": "Rental Admin",
    "welcome_sign": "Welcome to Rental Management Admin",
    "copyright": "Rental Management System 2026",
    
    # Navigation
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Icons for each model
    "icons": {
        "accounts.User": "fas fa-user",
        "properties.Property": "fas fa-building",
        "contracts.RentalContract": "fas fa-handshake",
        "billing.Bill": "fas fa-file-invoice-dollar",
        "payments.Payment": "fas fa-money-bill-wave",
        # ... and more
    },
    
    # Form layout
    "changeform_format": "horizontal_tabs",
    
    # App ordering
    "order_with_respect_to": [
        "accounts", "properties", "contracts",
        "billing", "payments", "audit"
    ]
}
```

### UI Theme (in `config/settings.py`)

```python
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "theme": "default",
    "navbar_fixed": True,
    "sidebar_fixed": True,
}
```

## Usage

### Accessing the Admin Panel

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Create a superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```

3. **Access the admin panel**:
   - URL: `http://localhost:8000/admin/`
   - Login with your superuser credentials

### Common Admin Tasks

#### Managing Users
- View all users with status badges
- Search by phone or email
- Filter by active status, staff status
- Bulk activate/deactivate users
- View user permissions and groups

#### Managing Properties
- Add new properties with locations
- Upload property photos
- Configure unit details and amenities
- Set rental terms and policies
- Track utility configurations

#### Managing Contracts
- Create new rental contracts
- Add participants (tenants and dependents)
- Set contract authors with permissions
- Terminate contracts with reasons
- View contract duration and financial terms

#### Managing Bills
- Create rent and utility bills
- Track payment status with progress bars
- View overdue bills
- Mark bills as paid
- Filter by billing month and status

#### Managing Payments
- View all payment transactions
- Track payment providers
- Monitor success/failure rates
- Process refunds
- View webhook events

#### Viewing Audit Logs
- Track all system changes
- View who made what changes
- Monitor IP addresses and user agents
- Filter by action type and entity
- Cannot be manually edited (data integrity)

## Best Practices

1. **Permissions**: Assign appropriate permissions to staff users
2. **Bulk Actions**: Use bulk actions for efficiency
3. **Filters**: Use filters to find specific records quickly
4. **Inline Editing**: Edit related objects inline when possible
5. **Audit Trail**: Review audit logs regularly for security
6. **Search**: Use search functionality for quick lookups
7. **Statistics**: Monitor summary statistics on list pages

## Security Features

- **Read-only audit logs**: Cannot be tampered with
- **Permission-based access**: Fine-grained control
- **Soft delete**: Users are soft-deleted, not permanently removed
- **Validation**: Form validation prevents invalid data
- **CSRF protection**: Django's built-in CSRF protection
- **SQL injection protection**: ORM prevents SQL injection

## Customization

### Adding Custom Actions

```python
@admin.action(description="Custom action")
def custom_action(self, request, queryset):
    # Your action logic here
    count = queryset.count()
    self.message_user(request, f"{count} items processed.")
```

### Adding Custom Filters

```python
class CustomFilter(admin.SimpleListFilter):
    title = 'filter title'
    parameter_name = 'param'
    
    def lookups(self, request, model_admin):
        return [('value', 'Label')]
    
    def queryset(self, request, queryset):
        if self.value() == 'value':
            return queryset.filter(field='value')
```

### Adding Custom Display Methods

```python
def custom_display(self, obj):
    return format_html('<span>{}</span>', obj.field)
custom_display.short_description = 'Custom Column'
```

## Troubleshooting

### Admin Panel Not Loading
- Check if Jazzmin is installed: `pip list | grep jazzmin`
- Verify INSTALLED_APPS has 'jazzmin' before 'django.contrib.admin'
- Run migrations: `python manage.py migrate`

### Models Not Showing
- Verify models are registered in admin.py
- Check import statements
- Restart development server

### Permission Errors
- Ensure user has appropriate permissions
- Check staff status is True
- Verify model permissions in Django admin

## Packages Installed

- `django-jazzmin==2.6.0` - Beautiful admin theme
- `django-phonenumber-field==7.3.0` - Phone number field validation
- `phonenumbers==8.13.27` - Phone number parsing library

## Summary

✅ All 15 models registered in admin panel
✅ Professional Bootstrap-based design
✅ Advanced filtering and search
✅ Inline editing for related models
✅ Custom actions for bulk operations
✅ Color-coded status badges
✅ Statistics and summaries
✅ Performance optimizations
✅ Mobile-responsive design
✅ Audit trail protection
✅ Permission-based access control

Your admin panel is now production-ready with a professional, user-friendly interface! 🎉

