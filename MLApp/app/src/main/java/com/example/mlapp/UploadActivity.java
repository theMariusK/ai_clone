package com.example.mlapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.VideoView;
import android.content.DialogInterface;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.MediaType;
import okhttp3.Response;
import android.widget.LinearLayout;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadActivity extends AppCompatActivity {

    private Button uploadButton;  // Button for uploading the file
    private Button deleteButton;  // Button for deleting the file
    private VideoView videoView;  // VideoView to show the recorded video
    private File recordedFile;    // File for the recorded video

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Initially set the content view with the layout that includes buttons for stop recording
        setContentView(R.layout.activity_upload);

        // Assume the file path for the recorded video (this could be passed via intent)
        recordedFile = new File(getExternalFilesDir(null), "recorded_video.mp4");

        // Initialize the VideoView and buttons
        videoView = findViewById(R.id.videoView);


        // Initially, these buttons should be hidden until the user stops recording
        uploadButton.setVisibility(View.GONE);
        deleteButton.setVisibility(View.GONE);

        // Set a click listener for the upload button
        uploadButton.setOnClickListener(v -> {
            if (recordedFile.exists()) {
                uploadFile(recordedFile);
            } else {
                Toast.makeText(this, "File not found", Toast.LENGTH_SHORT).show();
            }
        });

        // Set a click listener for the delete button
        deleteButton.setOnClickListener(v -> {
            deleteFile(recordedFile);
        });

        // You could add a listener for stop recording here (assuming you have it)
        // For example, you can show the video preview after the user stops recording
        // Here, we simulate this for testing purposes
        simulateStopRecording();
    }

    // This method is called after stopping the recording (simulated here)
    private void simulateStopRecording() {
        // Set the video path to the VideoView
        if (recordedFile.exists()) {
            videoView.setVideoPath(recordedFile.getAbsolutePath());
            videoView.start();  // Start playing the video
        }

        // Show the upload and delete buttons
        uploadButton.setVisibility(View.VISIBLE);
        deleteButton.setVisibility(View.VISIBLE);
    }


    //important
    // Upload the video to the server
    private void uploadFile(File file) {
        new Thread(() -> {
            try {
                OkHttpClient client = new OkHttpClient();

                MediaType mediaType = MediaType.parse("video/mp4");
                RequestBody fileBody = RequestBody.create(file, mediaType);

                MultipartBody requestBody = new MultipartBody.Builder()
                        .setType(MultipartBody.FORM)
                        .addFormDataPart("file", file.getName(), fileBody)
                        .build();

                Request request = new Request.Builder()
                        .url("http://127.0.0.1:5000/upload_video")
                        .post(requestBody)
                        .build();

                // Log the request details
                System.out.println("Uploading file: " + file.getAbsolutePath());

                Response response = client.newCall(request).execute();

                runOnUiThread(() -> {
                    if (response.isSuccessful()) {
                        Toast.makeText(this, "File uploaded successfully", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(this, "Upload failed: " + response.code(), Toast.LENGTH_SHORT).show();
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> Toast.makeText(this, "Upload failed", Toast.LENGTH_SHORT).show());
            }
        }).start();
    }



    // Delete the recorded video file
    private void deleteFile(File file) {
        boolean deleted = file.delete();
        if (deleted) {
            Toast.makeText(this, "File deleted successfully", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "Failed to delete file", Toast.LENGTH_SHORT).show();
        }
    }
}
