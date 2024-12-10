package com.example.mlapp;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.Camera;
import androidx.camera.core.CameraSelector;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.video.Quality;
import androidx.camera.video.QualitySelector;
import androidx.camera.video.Recorder;
import androidx.camera.video.Recording;
import androidx.camera.video.VideoCapture;
import androidx.camera.video.VideoRecordEvent;
import androidx.camera.video.FileOutputOptions;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.app.AlertDialog;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.VideoView;

import com.google.common.util.concurrent.ListenableFuture;

import java.io.File;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class RecordActivity extends AppCompatActivity {

    private Button startRecordingButton, stopRecordingButton;
    private androidx.camera.view.PreviewView previewView;
    private VideoCapture<Recorder> videoCapture;
    private Recording recording;
    private ExecutorService cameraExecutor;

    private File outputFile;

    private static final int REQUEST_CODE_PERMISSIONS = 101;
    private static final String[] REQUIRED_PERMISSIONS = {
            Manifest.permission.CAMERA,
            Manifest.permission.RECORD_AUDIO
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record);

        previewView = findViewById(R.id.previewView);
        startRecordingButton = findViewById(R.id.start_recording_button);
        stopRecordingButton = findViewById(R.id.stop_recording_button);
        stopRecordingButton.setVisibility(Button.GONE);

        cameraExecutor = Executors.newSingleThreadExecutor();

        if (allPermissionsGranted()) {
            startCamera();
        } else {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS);
        }

        startRecordingButton.setOnClickListener(v -> startRecording());
        stopRecordingButton.setOnClickListener(v -> stopRecording());
    }

    private boolean allPermissionsGranted() {
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    private void startCamera() {
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture = ProcessCameraProvider.getInstance(this);
        cameraProviderFuture.addListener(() -> {
            try {
                ProcessCameraProvider cameraProvider = cameraProviderFuture.get();
                CameraSelector cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA;

                androidx.camera.core.Preview preview = new androidx.camera.core.Preview.Builder().build();
                preview.setSurfaceProvider(previewView.getSurfaceProvider());

                QualitySelector qualitySelector = QualitySelector.from(Quality.HD);

                Recorder recorder = new Recorder.Builder()
                        .setQualitySelector(qualitySelector)
                        .build();

                videoCapture = VideoCapture.withOutput(recorder);

                Camera camera = cameraProvider.bindToLifecycle(
                        this,
                        cameraSelector,
                        preview,
                        videoCapture
                );
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(this, "Failed to start camera", Toast.LENGTH_SHORT).show();
            }
        }, ContextCompat.getMainExecutor(this));
    }

    @SuppressLint("MissingPermission")
    private void startRecording() {
        if (!allPermissionsGranted()) {
            Toast.makeText(this, "Permissions not granted", Toast.LENGTH_SHORT).show();
            return;
        }

        if (videoCapture == null) {
            Toast.makeText(this, "Video capture is not ready", Toast.LENGTH_SHORT).show();
            return;
        }

        outputFile = new File(getExternalFilesDir(null), "recorded_video.mp4");
        FileOutputOptions outputOptions = new FileOutputOptions.Builder(outputFile).build();

        recording = videoCapture.getOutput()
                .prepareRecording(this, outputOptions)
                .withAudioEnabled()
                .start(ContextCompat.getMainExecutor(this), videoRecordEvent -> {
                    if (videoRecordEvent instanceof VideoRecordEvent.Start) {
                        runOnUiThread(() -> {
                            startRecordingButton.setVisibility(Button.GONE);
                            stopRecordingButton.setVisibility(Button.VISIBLE);
                            Toast.makeText(this, "Recording started", Toast.LENGTH_SHORT).show();
                        });
                    } else if (videoRecordEvent instanceof VideoRecordEvent.Finalize) {
                        runOnUiThread(() -> {
                            stopRecordingButton.setVisibility(Button.GONE);
                            startRecordingButton.setVisibility(Button.VISIBLE);
                            Toast.makeText(this, "Recording saved: " + outputFile.getAbsolutePath(), Toast.LENGTH_LONG).show();
                            showVideoOptionsDialog(outputFile);
                        });
                    }
                });
    }

    private void stopRecording() {
        if (recording != null) {
            recording.stop();
            recording = null;
        }
    }

    private void showVideoOptionsDialog(File videoFile) {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.activity_upload, null);
        VideoView videoView = dialogView.findViewById(R.id.videoView);
        videoView.setVideoPath(videoFile.getAbsolutePath());
        videoView.start();

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setView(dialogView)
                .setCancelable(false)
                .setPositiveButton("Upload", (dialog, which) -> uploadVideo(videoFile))
                .setNegativeButton("Delete", (dialog, which) -> {
                    if (videoFile.exists()) {
                        videoFile.delete();
                        Toast.makeText(this, "Video deleted", Toast.LENGTH_SHORT).show();
                    }
                })
                .show();
    }

    private void uploadVideo(File videoFile) {
        if (!videoFile.exists()) {
            Toast.makeText(this, "File not found", Toast.LENGTH_SHORT).show();
            return;
        }

        new Thread(() -> {
            try {
                OkHttpClient client = new OkHttpClient();

                MediaType mediaType = MediaType.parse("video/mp4");
                RequestBody fileBody = RequestBody.create(videoFile, mediaType);

                MultipartBody requestBody = new MultipartBody.Builder()
                        .setType(MultipartBody.FORM)
                        .addFormDataPart("file", videoFile.getName(), fileBody)
                        .build();

                Request request = new Request.Builder()
                        .url("http://192.168.156.29:5000/upload_video")  // Replace with your actual server URL
                        .post(requestBody)
                        .build();

                Response response = client.newCall(request).execute();

                String responseBody = response.body() != null ? response.body().string() : "No response body";

                runOnUiThread(() -> {
                    if (response.isSuccessful()) {
                        Toast.makeText(this, "File uploaded successfully", Toast.LENGTH_SHORT).show();
                    } else {
                        // Log details for debugging
                        Toast.makeText(this, "Upload failed: " + response.code(), Toast.LENGTH_SHORT).show();
                        System.out.println("Upload failed. Code: " + response.code());
                        System.out.println("Response: " + responseBody);
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    Toast.makeText(this, "Upload failed", Toast.LENGTH_SHORT).show();
                    System.out.println("Upload failed due to exception: " + e.getMessage());
                });
            }
        }).start();
    }


    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (cameraExecutor != null) {
            cameraExecutor.shutdown();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                startCamera();
            } else {
                Toast.makeText(this, "Permissions not granted by the user.", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }
}
