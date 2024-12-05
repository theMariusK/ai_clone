package com.example.mlapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.OptIn;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.Camera;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ExperimentalGetImage;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.lifecycle.LifecycleOwner;
import com.google.common.util.concurrent.ListenableFuture;

public class MainActivity extends AppCompatActivity {

    private static final int CAMERA_REQUEST_CODE = 100;
    private PreviewView previewView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize PreviewView
        previewView = findViewById(R.id.previewView);

        // Check camera permission
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.CAMERA}, CAMERA_REQUEST_CODE);
        } else {
            // If permission granted, start camera
            startCamera();
        }
    }

    @OptIn(markerClass = ExperimentalGetImage.class)
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_REQUEST_CODE && grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            // Permission granted, start the camera
            startCamera();
        } else {
            // Permission denied, show a toast
            Toast.makeText(this, "Camera permission is required", Toast.LENGTH_SHORT).show();
        }
    }

    @OptIn(markerClass = ExperimentalGetImage.class)
    private void startCamera() {
        // Get the camera provider
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture = ProcessCameraProvider.getInstance(this);

        cameraProviderFuture.addListener(() -> {
            try {
                // Get the camera provider
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();

                // Set up Preview use case
                Preview preview = new Preview.Builder().build();
                preview.setSurfaceProvider(previewView.getSurfaceProvider());

                // Set up ImageAnalysis use case for face detection
                ImageAnalysis imageAnalysis = new ImageAnalysis.Builder()
                        .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                        .build();

                // Pass the BoundingBoxView to FaceAnalyzer
                FaceAnalyzer faceAnalyzer = new FaceAnalyzer(findViewById(R.id.boundingBoxView));

                imageAnalysis.setAnalyzer(ContextCompat.getMainExecutor(this), faceAnalyzer);

                // Select back camera
                CameraSelector cameraSelector = new CameraSelector.Builder()
                        .requireLensFacing(CameraSelector.LENS_FACING_FRONT)
                        .build();

                // Bind use cases to lifecycle
                cameraProvider.unbindAll(); // Unbind any previous use cases
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageAnalysis);
            } catch (Exception e) {
                Log.e("MainActivity", "Camera initialization failed", e);
                Toast.makeText(this, "Camera initialization failed", Toast.LENGTH_SHORT).show();
            }
        }, ContextCompat.getMainExecutor(this));
    }

}
