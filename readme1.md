# Hellbound Admin + Client System - Termux Guide

This comprehensive guide provides detailed instructions for setting up, running, and managing the Hellbound Admin + Client System within the Termux environment on Android devices. Termux offers a powerful and portable Linux-like environment directly on your smartphone or tablet, enabling you to host the Admin Panel and Backend server, and prepare client APKs, all from a mobile device.

## 🎯 Why Termux?

Termux transforms your Android device into a versatile development and administration platform. Its key advantages for the Hellbound system include:

-   **Portability**: Run the entire system from virtually anywhere, without needing a traditional desktop or laptop.
-   **Self-Contained Environment**: All necessary tools, dependencies, and project files are managed within the Termux application, minimizing external requirements.
-   **Accessibility**: Ideal for users who primarily work on mobile devices or require a highly portable solution for remote administration tasks.
-   **Cost-Effective**: Utilizes existing Android hardware, eliminating the need for dedicated server infrastructure for basic operations.

## 📋 Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Termux Setup](#termux-setup)
3.  [System Installation](#system-installation)
4.  [Running the System](#running-the-system)
5.  [Building Client APKs](#building-client-apks)
6.  [Managing Background Processes](#managing-background-processes)
7.  [Troubleshooting Termux-Specific Issues](#troubleshooting-termux-specific-issues)
8.  [Security Considerations on Termux](#security-considerations-on-termux)
9.  [Conclusion](#conclusion)

---

## 1. Prerequisites

Before you begin, ensure your Android device and Termux installation meet the following requirements:

### Android Device Requirements

-   **Operating System**: Android 7.0 (Nougat) or higher is recommended for optimal compatibility and performance. Older versions might have limited support for newer Termux features or packages.
-   **RAM**: A minimum of 3GB RAM is recommended for smooth operation of both the Flask backend and React frontend. Devices with 4GB RAM or more will provide a significantly better experience, especially when building the React frontend.
-   **Storage**: Ensure you have at least 2GB of free internal storage. This space is needed for Termux itself, its packages, Node.js and Python dependencies, and the Hellbound system project files. Building the React frontend can temporarily consume additional space.
-   **Internet Connection**: A stable internet connection is required for downloading Termux packages, Node.js and Python dependencies, and cloning the Hellbound system repository.

### Termux Application Requirements

-   **Termux Application**: Download and install the latest version of Termux from F-Droid or GitHub. **Avoid installing from Google Play Store** as it often contains outdated versions that may lead to compatibility issues with newer packages.
    -   **F-Droid**: [https://f-droid.org/packages/com.termux/](https://f-droid.org/packages/com.termux/)
    -   **GitHub Releases**: [https://github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)

-   **Termux:API (Optional but Recommended)**: Install the Termux:API add-on and the `termux-api` package within Termux. This allows access to various Android device features, including `termux-wake-lock` which is crucial for preventing background processes from being killed by Android's battery optimizations.
    ```bash
    pkg install termux-api
    ```

### General Knowledge

-   **Basic Linux Command Line**: Familiarity with basic Linux commands (e.g., `cd`, `ls`, `mkdir`, `chmod`) will be beneficial.
-   **Networking Concepts**: Understanding of IP addresses, ports, and basic client-server communication will help in configuring and troubleshooting the system.

---

## 2. Termux Setup

This section guides you through the initial setup of your Termux environment to prepare it for the Hellbound system.

### 2.1. Initial Termux Update

After installing Termux, it's crucial to update its package lists and installed packages to their latest versions. This ensures you have access to the most recent features and security patches.

```bash
pkg update -y && pkg upgrade -y
```

-   `pkg update -y`: Updates the list of available packages from the Termux repositories. The `-y` flag automatically confirms any prompts.
-   `pkg upgrade -y`: Upgrades all installed packages to their latest versions. Again, `-y` provides automatic confirmation.

### 2.2. Install Essential Development Tools

The Hellbound system requires several core development tools. Termux provides pre-compiled versions of these tools through its `pkg` package manager.

-   **Git**: For cloning the project repository.
    ```bash
    pkg install -y git
    ```

-   **Node.js and npm**: Required for the React frontend (Admin Panel).
    ```bash
    pkg install -y nodejs
    ```
    This command installs both Node.js and its package manager, npm.

-   **Python and pip**: Required for the Flask backend.
    ```bash
    pkg install -y python python-pip
    ```
    This installs Python 3 and `pip`, its package installer.

-   **OpenJDK 17**: Required for the `keytool` utility (for keystore generation) and for potential future Java-based tools. While the Android client is built externally, `keytool` is still used by the `build_apk.py` script to generate the keystore.
    ```bash
    pkg install -y openjdk-17
    ```

-   **Network Utilities**: `netcat` is useful for basic network testing and debugging.
    ```bash
    pkg install -y netcat
    ```

-   **Archiving Tools**: `unzip` and `zip` are necessary for handling compressed project files and the generated client project ZIPs.
    ```bash
    pkg install -y unzip zip
    ```

-   **Download Tools**: `curl` and `wget` are generally pre-installed but ensure they are available.
    ```bash
    pkg install -y curl wget
    ```

### 2.3. Verify Installations

After installing the packages, you can verify their successful installation by checking their versions:

```bash
node --version
python --version
java -version
git --version
```

If all commands return version numbers without errors, your Termux environment is ready for the Hellbound system installation.

---

## 3. System Installation

This section details how to install the Hellbound Admin + Client System project files into your Termux environment.

### 3.1. Clone the Repository

First, you need to clone the Hellbound system repository from its source. Navigate to your Termux home directory (which is the default directory when you open Termux) and clone the repository.

```bash
git clone <repository-url>
cd hellbound_system
```

Replace `<repository-url>` with the actual Git URL of the Hellbound system repository. For example, if it's hosted on GitHub, it would look like `https://github.com/yourusername/hellbound_system.git`.

### 3.2. Run the Termux-Adapted Setup Script

The Hellbound system includes a `setup.sh` script that automates the installation of project-specific dependencies and configurations. This script has been specifically adapted for the Termux environment.

Navigate into the cloned `hellbound_system` directory if you are not already there:

```bash
cd hellbound_system
```

Make the `setup.sh` script executable and then run it:

```bash
chmod +x setup.sh
./setup.sh
```

This script will perform the following actions:

-   **Install React Frontend Dependencies**: It will navigate to `Admin/HellboundAdmin` and run `npm install` to download and set up all necessary JavaScript packages for the web interface.
-   **Set Up Flask Backend**: It will create a Python virtual environment (`venv`) within `Admin/HellboundBackend`, activate it, and install Flask and Flask-CORS using `pip`. This isolates the Python dependencies for the backend.
-   **Generate APK Signing Keystore**: It will use `keytool` (from OpenJDK) to generate a `hellbound.keystore` file in the root of the `hellbound_system` directory. This keystore is essential for signing Android APKs. You will be prompted to enter a password and some details for the keystore. For simplicity, you can use `hellbound_password` as the password when prompted.
-   **Create Directories**: It will ensure the `output` and `logs` directories exist for storing generated APK project ZIPs and system logs, respectively.
-   **Create Environment File**: It will create a `.env` file with default configuration settings for the Flask backend and TCP server, including host, port, and keystore details.
-   **Make Scripts Executable**: It will ensure all necessary shell scripts (`setup.sh`, `start.sh`, `stop.sh`) are executable.

Upon successful completion, the script will display a success message and provide instructions for the next steps.

---

## 4. Running the System

Once the installation is complete, you can launch the Hellbound Admin + Client System components within Termux.

### 4.1. Launch the System Components

The `start.sh` script is designed to launch both the Flask backend and the React frontend in the background, allowing you to continue using your Termux terminal.

From the `hellbound_system` directory, make the `start.sh` script executable and run it:

```bash
chmod +x start.sh
./start.sh
```

This script will:

-   **Start Flask Backend**: It will activate the Python virtual environment and run `src/main.py` using `nohup` to ensure it continues running even if your Termux session is closed (though Android's battery optimizations might still interfere, see Section 6).
    -   The Flask backend will listen on `http://localhost:5000`.
    -   The TCP server for client connections will listen on `0.0.0.0:4444`.
-   **Start React Frontend**: It will navigate to the `Admin/HellboundAdmin` directory and run `npm run dev` using `nohup`. This starts the Vite development server for the Admin Panel.
    -   The React frontend will be accessible on `http://localhost:5173`.

After the script finishes, it will display the status of both components and their access points.

### 4.2. Access the Admin Panel

Once the `start.sh` script indicates that both the Flask backend and React frontend are running, you can access the Admin Panel from your Android device's web browser.

Open your preferred web browser (e.g., Chrome, Firefox) on your Android device and navigate to:

```
http://localhost:5173
```

You should see the Hellbound Admin Panel interface. From here, you can interact with the system, manage the server, view connected clients, and prepare client APK projects.

### 4.3. Verify Server Status

You can verify that the Flask backend and its integrated TCP server are running by checking the server status in the Admin Panel's 


Server Control tab, or by directly accessing the API endpoint:

```
http://localhost:5000/api/server/status
```

This endpoint should return a JSON response indicating whether the server is `running` and the `clients_count`.

---

## 5. Building Client APKs

**Important Note for Termux Users**: Due to the inherent limitations of Termux as a full-fledged Android SDK build environment, the `build_apk.py` script and the Admin Panel's 


APK Builder functionality within Termux will **only prepare the client project files** with the injected configuration (host, port, app name, package name). It will **not** compile the final `.apk` file directly.

This design choice is made because replicating a complete Android build environment (including Gradle, Android SDK tools like `aapt`, `dx`, `apksigner`, `zipalign`, and all their dependencies) within Termux is highly complex and often unstable. The primary purpose of running the system on Termux is to provide a portable administration interface and a convenient way to generate configured client projects.

To obtain the final, installable `.apk` file, you will follow a hybrid approach:

### 5.1. Prepare the Client Project using the Admin Panel (on Termux)

1.  **Access the Admin Panel**: Open your web browser on your Android device and navigate to `http://localhost:5173`.
2.  **Navigate to APK Builder**: Click on the "APK Builder" tab in the Admin Panel.
3.  **Configure Connection Settings**: 
    -   Enter the **Host IP Address**: This is the IP address where your Admin Panel (and its TCP server) will be accessible from the client device. If you are testing on the same Termux device, you can use `127.0.0.1` or `localhost`. If the client will be on a different device in your local network, use your Android device's local IP address (e.g., `192.168.1.X`). If the client is external, you might need a public IP or port forwarding.
    -   Enter the **Port**: This is the port the TCP server is listening on (default: `4444`).
4.  **Customize App Settings (Optional)**:
    -   **App Name**: This is the name that will appear in the Android device's system settings (e.g., "System Update").
    -   **Package Name**: This is the unique identifier for the Android application (e.g., `com.android.systemupdate`). Changing this can help avoid conflicts with existing apps.
5.  **Build Client Project**: Click the "Build Client APK" button. The backend will process your request, inject the configuration into the client project template, and package the modified project into a `.zip` file.
6.  **Download the ZIP**: The Admin Panel will provide a download link (e.g., `hellbound_client_192.168.1.100_4444.zip`). Download this `.zip` file to your Android device.

### 5.2. Build the Final APK on a Desktop Machine (with Android Studio)

Once you have the `.zip` file containing the configured Android client project, you need to transfer it to a desktop computer (Windows, macOS, or Linux) that has Android Studio installed.

1.  **Transfer the ZIP**: Transfer the downloaded `.zip` file from your Android device to your desktop computer. You can use various methods like USB cable, cloud storage (Google Drive, Dropbox), or `adb pull` if you have ADB set up.
2.  **Unzip the Project**: Extract the contents of the `.zip` file to a convenient location on your desktop. You will find a directory named `HellboundClient` (or similar, depending on the original project structure).
3.  **Open in Android Studio**: Launch Android Studio and select "Open an existing Android Studio project." Navigate to the unzipped `HellboundClient` directory and open it.
4.  **Build the Release APK**: Once the project is loaded and Gradle sync is complete, you can build the release APK.
    -   **Using Android Studio GUI**: Go to `Build > Build Bundles / APKs > Build APKs`.
    -   **Using Gradle Command Line**: Open a terminal or command prompt, navigate to the `HellboundClient` directory (the one containing `build.gradle`), and run:
        ```bash
        ./gradlew assembleRelease
        ```
        *On Windows, you might need to use `gradlew.bat assembleRelease`.*

5.  **Locate the APK**: The signed release APK will typically be found in the `HellboundClient/app/build/outputs/apk/release/` directory. The file name will usually be `app-release.apk` or `app-release-unsigned.apk` (if not signed by Gradle).

6.  **Sign the APK (if unsigned)**: If you built an unsigned APK, you will need to sign it using the `hellbound.keystore` generated by the `setup.sh` script (which is located in your Termux `hellbound_system` directory). Transfer this keystore to your desktop and use `jarsigner`.
    ```bash
    jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
              -keystore /path/to/your/hellbound.keystore \
              -storepass hellbound_password \
              -signedjar app-release-signed.apk \
              app-release-unsigned.apk hellbound_alias
    ```
    *Replace `/path/to/your/hellbound.keystore` with the actual path to your keystore file.*

7.  **Zipalign the APK (Recommended)**: For optimal performance and to ensure proper installation, zipalign the APK.
    ```bash
    zipalign -v 4 app-release-signed.apk app-release-final.apk
    ```
    *The `zipalign` tool is part of the Android SDK Build-Tools. Its path might be something like `~/Android/Sdk/build-tools/30.0.3/zipalign`.*

### 5.3. Install the APK on Android

Once you have the final, signed, and zipaligned `.apk` file, you can transfer it back to your Android device and install it. You can do this by simply tapping the `.apk` file in a file manager on your Android device, or by using `adb install` from your desktop if you have ADB set up.

---




## 6. Managing Background Processes on Termux

When running server-side applications like the Flask backend and its integrated TCP server on Termux, it's crucial to understand how Android manages background processes. By default, Android's battery optimization features might kill background applications to conserve power, which can lead to your Hellbound system components unexpectedly stopping.

Here are strategies to ensure the stability and persistence of your system on Termux:

### 6.1. Using `termux-wake-lock`

The `termux-wake-lock` utility is part of the `termux-api` package and is the most effective way to prevent Termux from being killed by Android's system. It acquires a partial wake lock, which keeps the CPU running even when the screen is off, ensuring that background processes continue to execute.

1.  **Install `termux-api` (if you haven't already)**:
    ```bash
    pkg install termux-api
    ```

2.  **Acquire Wake Lock**: Before starting your Hellbound system (or in a separate Termux session), run:
    ```bash
    termux-wake-lock
    ```
    You will see a persistent notification from Termux indicating that a wake lock is active. This notification signifies that Termux is actively preventing the device from going into deep sleep, thus allowing your background processes to run continuously.

3.  **Release Wake Lock**: When you are finished running the Hellbound system and want to allow your device to go into deep sleep, run:
    ```bash
    termux-wake-unlock
    ```
    The persistent notification will disappear, and Android will resume its normal battery optimization behavior.

    **Recommendation**: Always use `termux-wake-lock` when running the Hellbound system for extended periods to ensure maximum uptime and reliability.

### 6.2. Disabling Battery Optimization for Termux

While `termux-wake-lock` is effective, you can also manually configure your Android device to exclude Termux from battery optimizations. This can provide an additional layer of persistence, though the exact steps may vary slightly depending on your Android version and device manufacturer.

General steps:

1.  Go to your device's **Settings**.
2.  Navigate to **Apps & notifications** (or similar).
3.  Find and select **Termux** from the list of installed apps.
4.  Tap on **Battery** (or **Battery optimization**, **Power usage**).
5.  Select **Battery optimization** (or **Unrestricted**, **Don't optimize**).
6.  Find Termux in the list and set it to **Don't optimize** or **Unrestricted**.

    **Note**: Even with battery optimization disabled, Android might still kill processes under extreme memory pressure or after long periods of inactivity. `termux-wake-lock` remains the most reliable method for continuous operation.

### 6.3. Using `nohup` and `&` for Background Execution

The `start.sh` script already uses `nohup` and `&` to run the Flask backend and React frontend in the background. This ensures that the processes continue to run even if you close the Termux session (the terminal window), as long as the Termux application itself remains active and not killed by the system.

-   `nohup`: Prevents processes from being terminated when the controlling terminal is closed.
-   `&`: Runs the command in the background, returning control to the terminal immediately.

Example from `start.sh`:
```bash
nohup python src/main.py > ../logs/flask.log 2>&1 &
```
This command runs the Flask backend in the background, redirects its output to 