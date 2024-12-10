// BoundingBoxView.java
package com.example.mlapp;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.View;

import java.util.List;

public class BoundingBoxView extends View {
    private List<Rect> faceBoundingBoxes;
    private Paint paint;

    public BoundingBoxView(Context context, AttributeSet attrs) {
        super(context, attrs);
        paint = new Paint();
        paint.setColor(0xFFFF0000); // Red color for bounding box
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(8);
    }

    public void setFaceBoundingBoxes(List<Rect> boundingBoxes) {
        this.faceBoundingBoxes = boundingBoxes;
        invalidate(); // Request a redraw
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (faceBoundingBoxes != null) {
            for (Rect rect : faceBoundingBoxes) {
                canvas.drawRect(rect, paint);
            }
        }
    }
}
