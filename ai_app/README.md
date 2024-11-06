# ai_app client side

A new Flutter project.

## Getting Started

This Flutter project includes various dependencies and setup configurations for both Android and Flutter. Follow the steps below to ensure the project is configured correctly.

### Requirements

- **Flutter SDK**: Make sure Flutter is installed and set up on your machine.
- **Android SDK**: Ensure you have the required Android SDK components installed.
- **Java**: Java 17 is required for this project.

### Project Setup

1. **Dependencies**

   Open the `pubspec.yaml` file and verify that the following dependencies are included under `dependencies`. If they are not, add them as shown below:

   ```yaml
   dependencies:
     flutter:
       sdk: flutter
     camera: ^0.11.0+2
     video_player: ^2.9.2
     open_file: ^3.5.9

    After making any changes to the dependencies, run the following command to install them:

        flutter pub get

   ```

2. **Android Configuration**

   - open the file android/app/build.gradle and add the following

   ```
   android {
   ndkVersion "25.1.8937393"

   compileOptions {
       sourceCompatibility JavaVersion.VERSION_17
       targetCompatibility JavaVersion.VERSION_17
       }


   kotlinOptions {
       jvmTarget = "17"
   }

   defaultConfig {
       minSdkVersion 21
   }
   }

   ```

   - add the following snippets in settings.gradle file :

   ```
   id "com.android.application" version "8.3.2" apply false
   id "org.jetbrains.kotlin.android" version "2.0.20" apply false

   ```

   - add the following code in gradle-wrapper.properties file :

   ```
    distributionUrl=https\://services.gradle.org/distributions/gradle-8.10.2-all.zip

   ```

### Running the Project

To build and run the project:

1. Connect a Device: Ensure a physical device or emulator is connected.

2. Run the App: Use the following command to start the app:
