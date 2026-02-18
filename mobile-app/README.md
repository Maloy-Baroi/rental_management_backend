# RentalBridge Mobile App

A cross-platform mobile application for rental property management built with React Native (Expo) and TypeScript.

## 🚀 Features

### For House Owners
- 📊 Dashboard with pending rent overview
- 🏠 Property and unit management
- 📝 Create "For Rent" posts
- 💰 Bill generation and management
- 👥 Tenant management
- 🔔 Tenant notifications

### For Tenants
- 📅 Payment due dates and reminders
- 🏘️ Browse available rental properties
- 💳 Multiple payment methods (bKash, Nagad, Rocket, Bank Transfer)
- 🧾 Download payment receipts
- 📊 Payment history

## 🛠️ Tech Stack

- **Framework**: Expo (SDK 51) with React Native 0.74
- **Language**: TypeScript
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **Navigation**: Expo Router (File-based routing)
- **State Management**: React Context API
- **API Client**: Axios with JWT interceptors
- **Storage**: expo-secure-store for tokens

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)
- For iOS: Xcode (Mac only)
- For Android: Android Studio

### Setup

1. **Install dependencies:**
```bash
cd mobile-app
npm install
```

2. **Configure API endpoint:**
   
Edit `src/api/client.ts` and update the `API_BASE_URL`:
```typescript
const API_BASE_URL = 'http://your-backend-url.com/api/v1';
```

For local development:
- Android Emulator: `http://10.0.2.2:8000/api/v1`
- iOS Simulator: `http://localhost:8000/api/v1`
- Physical Device: `http://YOUR_IP:8000/api/v1`

3. **Start the development server:**
```bash
npm start
```

4. **Run on device/emulator:**
```bash
# iOS
npm run ios

# Android
npm run android

# Web
npm run web
```

## 📁 Project Structure

```
mobile-app/
├── app/                    # Expo Router (File-based routes)
│   ├── (auth)/            # Authentication screens
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/            # Tab-based navigation
│   │   ├── dashboard/
│   │   ├── properties/
│   │   ├── browse/
│   │   ├── payments/
│   │   └── profile/
│   └── _layout.tsx        # Root layout
├── src/
│   ├── api/               # API client and services
│   │   ├── client.ts
│   │   └── services/
│   ├── components/        # Reusable UI components
│   │   └── ui/
│   ├── context/           # React Context (Auth, etc.)
│   ├── hooks/             # Custom React hooks
│   └── types/             # TypeScript interfaces
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## 🔐 Authentication Flow

1. User opens the app
2. If not authenticated → Redirect to Login
3. After login → Store JWT tokens in secure storage
4. Navigate to Dashboard (role-based)
5. API requests automatically include JWT token
6. On 401 error → Attempt token refresh
7. If refresh fails → Redirect to Login

## 🎨 UI Components

### Available Components

- `Button`: Primary, secondary, outline, danger variants
- `Input`: Text input with labels, errors, icons
- `Card`: Container with elevation/outline variants
- `Skeleton`: Loading placeholders

### Usage Example

```tsx
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';

<Card variant="elevated">
  <CardHeader title="Dashboard" subtitle="Welcome back" />
  <CardContent>
    <Button title="Get Started" onPress={handlePress} />
  </CardContent>
</Card>
```

## 🔌 API Integration

### Making API Calls

```typescript
import { propertyService } from '@/api/services/property.service';

// Get properties
const properties = await propertyService.getProperties();

// Create property
const newProperty = await propertyService.createProperty({
  house_name: 'Building A',
  total_floors: 5,
  // ... other fields
});
```

### Available Services

- `authService`: Login, register, profile, logout
- `propertyService`: Properties and units CRUD
- `billingService`: Bills management
- `paymentService`: Payments and receipts
- `dashboardService`: Dashboard statistics

## 🚦 Protected Routes

Routes are automatically protected based on authentication status:

- Unauthenticated users → Redirected to `/login`
- Authenticated users trying to access auth screens → Redirected to `/dashboard`
- Role-based tab visibility (Owner vs Tenant)

## 🎭 Role-Based Features

### House Owner Tabs
- Dashboard
- Properties
- Tenants
- Billing
- Profile

### Tenant Tabs
- Dashboard
- Browse
- Payments
- Profile

## 📱 Development Tips

### Testing on Different Devices

**Android Emulator:**
```bash
# Start emulator first, then:
npm run android
```

**iOS Simulator (Mac only):**
```bash
npm run ios
```

**Physical Device:**
1. Install Expo Go app from App Store/Play Store
2. Scan QR code from terminal
3. Make sure device and computer are on same network

### Hot Reload

- Shake device or press `Cmd+D` (iOS) / `Cmd+M` (Android)
- Enable Fast Refresh for instant updates

### Debugging

1. **Chrome DevTools:**
   - Press `j` in terminal to open debugger
   
2. **React DevTools:**
   ```bash
   npm install -g react-devtools
   react-devtools
   ```

3. **Network Requests:**
   - Use Flipper for advanced debugging

## 🔧 Configuration

### Update Backend URL

Edit `src/api/client.ts`:
```typescript
const API_BASE_URL = __DEV__ 
  ? 'http://10.0.2.2:8000/api/v1'  // Development
  : 'https://api.rentalbridge.com/api/v1';  // Production
```

### Customize Theme

Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#2196f3',
        // ... other shades
      }
    }
  }
}
```

## 📦 Building for Production

### Android (APK/AAB)

```bash
# Build APK
eas build --platform android --profile preview

# Build AAB for Play Store
eas build --platform android --profile production
```

### iOS (IPA)

```bash
# Build for App Store
eas build --platform ios --profile production
```

### Setup EAS Build

```bash
npm install -g eas-cli
eas login
eas build:configure
```

## 🧪 Testing

### Run Type Check

```bash
npm run type-check
```

### Lint Code

```bash
npm run lint
```

## 🐛 Troubleshooting

### Common Issues

**"Unable to connect to backend"**
- Check API_BASE_URL is correct
- Ensure backend is running
- For Android emulator, use `10.0.2.2` instead of `localhost`

**"Module not found"**
```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npx expo start -c
```

**"Build failed"**
```bash
# Clean and rebuild
npx expo prebuild --clean
```

## 📚 Additional Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/)
- [NativeWind Documentation](https://www.nativewind.dev/)
- [Expo Router Documentation](https://docs.expo.dev/router/introduction/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is part of the RentalBridge system.

## 🆘 Support

For issues and questions:
- Check existing documentation
- Review backend API documentation at `/api/docs/`
- Contact the development team

---

**Happy Coding! 🚀**

