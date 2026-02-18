# RentalBridge Mobile App - Quick Setup Guide

## 🎯 What Has Been Created

A complete **React Native (Expo)** mobile application foundation with:

✅ **Authentication System**
- Login & Registration screens
- JWT token management with auto-refresh
- Protected routes based on authentication
- Secure token storage using expo-secure-store

✅ **Role-Based Navigation**
- Dynamic tabs based on user role (Owner vs Tenant)
- Owner Dashboard: Properties, Tenants, Billing
- Tenant Dashboard: Browse, Payments

✅ **API Integration Layer**
- Axios client with JWT interceptors
- Service modules for Auth, Properties, Billing, Payments
- Automatic token refresh on 401 errors
- TypeScript interfaces for all API responses

✅ **Modern UI Components**
- Button (with variants and loading states)
- Input (with validation and error handling)
- Card (with header and content sections)
- Loading Skeletons
- NativeWind (Tailwind CSS) styling

✅ **Dashboard Screens**
- Owner Dashboard: Pending rent, property stats, quick actions
- Tenant Dashboard: Next payment, rental info, payment history
- Pull-to-refresh functionality

## 📋 Prerequisites

Before you start, ensure you have:

1. **Node.js 18+** installed
   ```bash
   node --version
   ```

2. **npm or yarn**
   ```bash
   npm --version
   ```

3. **Expo CLI** (optional but recommended)
   ```bash
   npm install -g expo-cli
   ```

4. **Development Environment:**
   - **For iOS**: Mac with Xcode installed
   - **For Android**: Android Studio with Android SDK
   - **Alternative**: Expo Go app on your phone

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
cd mobile-app
npm install
```

This will install:
- Expo SDK 51
- React Native 0.74
- TypeScript
- NativeWind (Tailwind)
- Axios
- React Navigation
- All other dependencies

### Step 2: Configure Backend URL

Open `src/api/client.ts` and update the API endpoint:

```typescript
const API_BASE_URL = __DEV__ 
  ? 'http://10.0.2.2:8000/api/v1'  // Android emulator
  : 'https://your-production-api.com/api/v1';
```

**Important Notes:**
- **Android Emulator**: Use `10.0.2.2` (points to host machine's localhost)
- **iOS Simulator**: Use `localhost:8000` or `127.0.0.1:8000`
- **Physical Device**: Use your computer's IP address (e.g., `192.168.1.100:8000`)
  - Find your IP: `ifconfig` (Mac/Linux) or `ipconfig` (Windows)
  - Make sure device and computer are on the same network

### Step 3: Start Development Server

```bash
npm start
```

This will:
1. Start the Metro bundler
2. Show a QR code
3. Display options to run on different platforms

### Step 4: Run on Device/Emulator

**Option A: Using Expo Go (Easiest)**
1. Install "Expo Go" app from App Store (iOS) or Play Store (Android)
2. Scan the QR code from terminal
3. App will load on your device

**Option B: Using Emulator/Simulator**

For Android:
```bash
npm run android
```

For iOS (Mac only):
```bash
npm run ios
```

For Web (for testing):
```bash
npm run web
```

## 🔧 Backend Requirements

### 1. Add User Role Field

The mobile app expects a `role` field on the User model. Update your backend:

```python
# apps/accounts/models.py
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('owner', 'House Owner'),
        ('tenant', 'Tenant'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='tenant'
    )
    # ...existing fields...
```

### 2. Add Dashboard Stats Endpoint

Create a view that returns dashboard statistics:

```python
# apps/properties/views.py
from rest_framework.decorators import action

class PropertyViewSet(viewsets.ModelViewSet):
    # ...existing code...
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        user = request.user
        if user.role == 'owner':
            return Response({
                'total_properties': Property.objects.filter(created_by=user).count(),
                'total_units': Unit.objects.filter(property__created_by=user).count(),
                'occupied_units': Unit.objects.filter(
                    property__created_by=user, 
                    is_available=False
                ).count(),
                'vacant_units': Unit.objects.filter(
                    property__created_by=user, 
                    is_available=True
                ).count(),
                'pending_rent_amount': calculate_pending_rent(user),
                'pending_rent_count': Bill.objects.filter(
                    contract__unit__property__created_by=user,
                    status='pending'
                ).count(),
                'total_tenants': Contract.objects.filter(
                    unit__property__created_by=user,
                    status='active'
                ).values('tenant').distinct().count(),
            })
        elif user.role == 'tenant':
            current_contract = Contract.objects.filter(
                tenant=user,
                status='active'
            ).first()
            
            next_payment = Bill.objects.filter(
                contract=current_contract,
                status='pending'
            ).order_by('due_date').first()
            
            return Response({
                'current_contract': ContractSerializer(current_contract).data if current_contract else None,
                'next_payment': {
                    'bill_id': next_payment.id,
                    'amount': next_payment.total_amount,
                    'due_date': next_payment.due_date,
                    'days_remaining': (next_payment.due_date - timezone.now().date()).days
                } if next_payment else None,
                'total_paid': Payment.objects.filter(
                    bill__contract__tenant=user,
                    status='completed'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'last_payment': PaymentSerializer(
                    Payment.objects.filter(
                        bill__contract__tenant=user,
                        status='completed'
                    ).order_by('-payment_date').first()
                ).data if Payment.objects.filter(
                    bill__contract__tenant=user,
                    status='completed'
                ).exists() else None,
            })
```

### 3. Update Registration Endpoint

Ensure registration accepts `role` field:

```python
# apps/accounts/serializers.py
class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[('owner', 'House Owner'), ('tenant', 'Tenant')],
        default='tenant'
    )
    
    class Meta:
        model = User
        fields = ['phone', 'email', 'password', 'role']
        # ...
```

### 4. Enable CORS for Mobile App

```python
# config/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # Expo dev server
    "http://127.0.0.1:8081",
]

# Or for development (not recommended for production):
CORS_ALLOW_ALL_ORIGINS = True
```

## 🧪 Testing the App

### 1. Test Login Flow

1. Start your Django backend
2. Start the mobile app
3. You should see the login screen
4. Try logging in with existing credentials
5. On successful login, you'll be redirected to the dashboard

### 2. Test Registration

1. Click "Sign Up" on login screen
2. Fill in the form
3. Select role (Tenant or House Owner)
4. Submit registration
5. You should be auto-logged in and see the dashboard

### 3. Test Role-Based Navigation

**As Owner:**
- Dashboard should show: Pending rent, properties stats, quick actions
- Tabs: Dashboard, Properties, Tenants, Billing, Profile

**As Tenant:**
- Dashboard should show: Next payment, rental info, payment history
- Tabs: Dashboard, Browse, Payments, Profile

## 📱 Development Tips

### Hot Reload

The app supports hot reload. Just save your files and changes will appear instantly!

### Debugging

**Open Developer Menu:**
- iOS Simulator: Press `Cmd + D`
- Android Emulator: Press `Cmd + M` or `Ctrl + M`
- Physical Device: Shake the device

**View Logs:**
```bash
# In the terminal where you ran `npm start`
# Logs will appear automatically
```

**React DevTools:**
```bash
npm install -g react-devtools
react-devtools
```

### Clear Cache

If you encounter issues:
```bash
npx expo start -c
```

## 📂 Project Structure Explanation

```
mobile-app/
├── app/                          # Expo Router (File = Route)
│   ├── _layout.tsx              # Root layout with auth logic
│   ├── (auth)/                  # Auth group (unprotected)
│   │   ├── _layout.tsx
│   │   ├── login.tsx            # /login
│   │   └── register.tsx         # /register
│   └── (tabs)/                  # Protected tabs
│       ├── _layout.tsx          # Tab navigation
│       ├── dashboard/
│       │   └── index.tsx        # /(tabs)/dashboard
│       ├── properties/
│       ├── browse/
│       ├── payments/
│       └── profile/
│
├── src/
│   ├── api/
│   │   ├── client.ts            # Axios instance with interceptors
│   │   └── services/            # API service modules
│   │       ├── auth.service.ts
│   │       ├── property.service.ts
│   │       ├── billing.service.ts
│   │       └── payment.service.ts
│   │
│   ├── components/
│   │   └── ui/                  # Reusable UI components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Card.tsx
│   │       └── LoadingSkeleton.tsx
│   │
│   ├── context/
│   │   └── AuthContext.tsx      # Auth state management
│   │
│   └── types/
│       └── index.ts             # TypeScript interfaces
│
├── package.json
├── tsconfig.json
├── tailwind.config.js           # Tailwind theme config
└── app.json                     # Expo configuration
```

## 🎨 Customizing the UI

### Change Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#YOUR_COLOR',
        // ...
      }
    }
  }
}
```

### Add New Component

```typescript
// src/components/ui/MyComponent.tsx
import React from 'react';
import { View, Text } from 'react-native';

export const MyComponent = ({ title }: { title: string }) => {
  return (
    <View className="p-4 bg-white rounded-lg">
      <Text className="text-lg font-bold">{title}</Text>
    </View>
  );
};
```

### Use Component

```typescript
import { MyComponent } from '@/components/ui/MyComponent';

<MyComponent title="Hello World" />
```

## 🐛 Common Issues

### "Unable to resolve module"

```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npx expo start -c
```

### "Network request failed"

1. Check backend is running
2. Verify API_BASE_URL is correct
3. For Android emulator, use `10.0.2.2` not `localhost`
4. For physical device, use computer's IP address

### "Unexpected token" or syntax errors

Make sure you're using the correct Node version:
```bash
node --version  # Should be 18+
```

### Build fails on iOS

```bash
cd ios
pod install
cd ..
npm run ios
```

## 📦 Next Steps

Now that your app foundation is ready:

1. **Test the authentication flow** with your backend
2. **Implement remaining screens**:
   - Properties list and detail
   - Browse available units
   - Payment submission
   - Receipt download
3. **Add image upload** for properties
4. **Implement push notifications** (Firebase)
5. **Add unit tests**
6. **Polish UI/UX**
7. **Prepare for deployment**

## 📚 Additional Features to Implement

### Properties Screen (Owner)
- List all properties with photos
- Add new property form
- Edit/delete properties
- View units in each property

### Browse Screen (Tenant)
- Grid/List of available rentals
- Search and filter
- Property details with photos
- Contact owner

### Payments Screen (Tenant)
- List of bills (pending, paid, overdue)
- Payment form with multiple methods
- Payment history
- Download receipts

### Billing Screen (Owner)
- Generate bills
- View all bills
- Filter by status
- Send reminders

## 🆘 Need Help?

1. Check the comprehensive README.md
2. Review the MOBILE_APP_GUIDE.md
3. Check Expo documentation: https://docs.expo.dev/
4. Review your backend Swagger docs: http://localhost:8000/api/docs/

## 🎉 You're All Set!

Your RentalBridge mobile app foundation is ready. Start the development server and begin building amazing features!

```bash
cd mobile-app
npm install
npm start
```

**Happy Coding! 🚀**

