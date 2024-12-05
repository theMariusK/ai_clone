package com.example.mlapp;

import android.graphics.Matrix;
import android.graphics.Rect;
import android.util.Log;
import androidx.annotation.NonNull;
import androidx.camera.core.ImageAnalysis;
import androidx.camera.core.ImageProxy;
import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.face.Face;
import com.google.mlkit.vision.face.FaceDetection;
import com.google.mlkit.vision.face.FaceDetector;
import com.google.mlkit.vision.face.FaceDetectorOptions;

import java.util.ArrayList;
import java.util.List;

@androidx.camera.core.ExperimentalGetImage
public class FaceAnalyzer implements ImageAnalysis.Analyzer {

    private final FaceDetector faceDetector;
    private final BoundingBoxView boundingBoxView; // Reference to the custom view

    public FaceAnalyzer(BoundingBoxView boundingBoxView) {
        this.boundingBoxView = boundingBoxView;

        // Configure face detector options
        FaceDetectorOptions options = new FaceDetectorOptions.Builder()
                .setPerformanceMode(FaceDetectorOptions.PERFORMANCE_MODE_FAST)
                .setLandmarkMode(FaceDetectorOptions.LANDMARK_MODE_ALL)
                .setClassificationMode(FaceDetectorOptions.CLASSIFICATION_MODE_ALL)
                .build();

        faceDetector = FaceDetection.getClient(options);
    }

    @Override
    public void analyze(@NonNull ImageProxy imageProxy) {
        try {
            if (imageProxy.getImage() == null) {
                imageProxy.close();
                return;
            }

            // Convert ImageProxy to InputImage
            InputImage image = InputImage.fromMediaImage(imageProxy.getImage(), imageProxy.getImageInfo().getRotationDegrees());

            // Process the image
            faceDetector.process(image)
                    .addOnSuccessListener(faces -> {
                        List<Rect> boundingBoxes = new ArrayList<>();
                        for (Face face : faces) {
                            Log.d("FaceAnalyzer", "Face detected with bounds: " + face.getBoundingBox());
                            if (face.getSmilingProbability() != null) {
                                Log.d("FaceAnalyzer", "Smiling probability: " + face.getSmilingProbability());
                            }
                            Rect transformedBoundingBox = transformBoundingBox(face.getBoundingBox(), imageProxy, boundingBoxView);
                            boundingBoxes.add(transformedBoundingBox);                         }
                        // Update the BoundingBoxView with the detected face bounding boxes
                        boundingBoxView.setFaceBoundingBoxes(boundingBoxes);
                    })
                    .addOnFailureListener(e -> Log.e("FaceAnalyzer", "Face detection failed", e))
                    .addOnCompleteListener(task -> imageProxy.close());
        } catch (Exception e) {
            imageProxy.close();
        }
    }
//    Transforms the bounding box coordinates from the image space to the view space.
     /**
      * @param boundingBox the bounding box from the face detector.
      * @param imageProxy  the image proxy containing the camera image.
      * @param boundingBoxView the view that will display the bounding boxes.
      * @return the transformed bounding box in the correct coordinates for the PreviewView.
      */
     private Rect transformBoundingBox(Rect boundingBox, ImageProxy imageProxy, BoundingBoxView boundingBoxView) {
         // Get the width and height of the image and PreviewView
         int imageWidth = imageProxy.getWidth();
         int imageHeight = imageProxy.getHeight();
         int viewWidth = boundingBoxView.getWidth();
         int viewHeight = boundingBoxView.getHeight();

         // Determine the scaling mode (maintain aspect ratio)
         float scaleX = (float) viewWidth / imageWidth;
         float scaleY = (float) viewHeight / imageHeight;
         float scale = Math.min(scaleX, scaleY);

         // Calculate offset to center the image
         float offsetX = (viewWidth - imageWidth * scale) / 2f;
         float offsetY = (viewHeight - imageHeight * scale) / 2f;

         // Transform bounding box coordinates
         float left = boundingBox.left * scale + offsetX;
         float top = boundingBox.top * scale + offsetY;
         float right = boundingBox.right * scale + offsetX;
         float bottom = boundingBox.bottom * scale + offsetY;

         // Apply rotation
         int rotationDegrees = imageProxy.getImageInfo().getRotationDegrees();
         float[] points = {left, top, right, bottom};
         Matrix rotationMatrix = new Matrix();

         switch (rotationDegrees) {
             case 90:
                 rotationMatrix.postRotate(90, viewWidth / 2f, viewHeight / 2f);
                 break;
             case 180:
                 rotationMatrix.postRotate(180, viewWidth / 2f, viewHeight / 2f);
                 break;
             case 270:
                 rotationMatrix.postRotate(270, viewWidth / 2f, viewHeight / 2f);
                 break;
         }

         rotationMatrix.mapPoints(points);

         // Ensure bounding box stays within view
         left = Math.max(0, Math.min(viewWidth, Math.min(points[0], points[2])));
         top = Math.max(0, Math.min(viewHeight, Math.min(points[1], points[3])));
         right = Math.max(0, Math.min(viewWidth, Math.max(points[0], points[2])));
         bottom = Math.max(0, Math.min(viewHeight, Math.max(points[1], points[3])));

         Log.d("FaceAnalyzer", "Transformed Bounding Box - " +
                 "Original: " + boundingBox +
                 ", Rotated: (" + left + ", " + top + " - " + right + ", " + bottom + ")");

         return new Rect((int) left, (int) top, (int) right, (int) bottom);
     }

}
