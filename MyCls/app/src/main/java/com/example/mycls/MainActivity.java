package com.example.mycls;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import android.Manifest;


import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;

import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.jetbrains.annotations.NotNull;
import org.pytorch.IValue;
import org.pytorch.Module;
import org.pytorch.Tensor;
import org.pytorch.torchvision.TensorImageUtils;

import java.io.FileNotFoundException;
import java.io.IOException;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Array;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{
    TextView textView = null;
    ImageView imageview = null;
    ImageView camera = null;
    ImageView album = null;
    ImageView scan = null;

    Bitmap bitmap = null;
    Uri imageUri = null;
    Module module = null;

    private static final int PICK_IMAGE_REQUEST = 1;
    private static final int SHOOT_IMAGE_REQUEST = 2;
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 3;
    float threshold = 0.1f;
    int hasImage = 0;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 获取文本框、图片框
        textView = (TextView) findViewById(R.id.textView);
        imageview = (ImageView) findViewById(R.id.imageView);
        camera = (ImageView) findViewById(R.id.imageView2);
        album = (ImageView) findViewById(R.id.imageView3);
        scan = (ImageView) findViewById(R.id.imageView4);

        // 获取info


        // 绑定事件


        camera.setOnClickListener(this);
        album.setOnClickListener(this);
        scan.setOnClickListener(this);

        try {
            module = Module.load(assetFilePath(this, "cls_13.pt"));
            bitmap = BitmapFactory.decodeStream(getAssets().open("background.jpg"));
            imageview.setImageBitmap(bitmap);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Copies specified asset to the file in /files app directory and returns this file absolute path.
     *
     * @return absolute file path
     */
    public static String assetFilePath(Context context, String assetName) throws IOException {
        File file = new File(context.getFilesDir(), assetName);
        if (file.exists() && file.length() > 0) {
            return file.getAbsolutePath();
        }

        try (InputStream is = context.getAssets().open(assetName)) {
            try (OutputStream os = new FileOutputStream(file)) {
                byte[] buffer = new byte[4 * 1024];
                int read;
                while ((read = is.read(buffer)) != -1) {
                    os.write(buffer, 0, read);
                }
                os.flush();
            }
            return file.getAbsolutePath();
        }
    }

    public void onClick(View v){
        if(R.id.imageView4== v.getId()){  // 检测图片（将图片输入给模型）
            textView.setText("请选择一张图片");
            detectImage();
        }
        else if(R.id.imageView3 == v.getId()){  // 选取图片
            try {
                selectImage();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        else if(R.id.imageView2 == v.getId()){  // 拍照
            try {
                if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
                } else {
                    shootImage();
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }

    public void selectImage() throws IOException {
        Intent chooseIntent = new Intent(Intent.ACTION_GET_CONTENT);  // 打开文件
        chooseIntent.setType("image/*");  // 打开相册
        chooseIntent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(chooseIntent, PICK_IMAGE_REQUEST);
    }

    public void detectImage(){
        // 读取界面中的bitmap图片，把他变成tensor类型
        if(hasImage == 1){
            float[] MEAN_RGB = new float[]{0.5F, 0.5F, 0.5F};
            float[] STD_RGB = new float[]{0.5F, 0.5F, 0.5F};
            Tensor inputTensor = TensorImageUtils.bitmapToFloat32Tensor(bitmap, MEAN_RGB, STD_RGB);
            Tensor outputTensor = module.forward(IValue.from(inputTensor)).toTensor();
            float[] scores = outputTensor.getDataAsFloatArray();
            Log.d("11111111", "scores:" + Arrays.toString(scores));

//            // 使用softmax函数计算每个类别的概率
            scores = softmax(scores);
            Log.d("22222222", "scores:" + Arrays.toString(scores));
//
            float maxScore = -Float.MAX_VALUE;
            float secondMaxScore = -Float.MAX_VALUE;
            int maxScoreIdx = -1;
            int secondMaxIdx = -1;
            for (int i = 0; i < scores.length; i++) {
//                if (scores[i] > maxScore) {  // 这是只选择最可能的
//                    maxScore = scores[i];
//                    maxScoreIdx = i;
//                }
                if (scores[i] > maxScore) {  // 选择第一第二
                    secondMaxScore = maxScore;
                    secondMaxIdx = maxScoreIdx;
                    maxScore = scores[i];
                    maxScoreIdx = i;
                } else if (scores[i] > secondMaxScore) {
                    secondMaxScore = scores[i];
                    secondMaxIdx = i;
                }
            }
//            Log.d("33333333", "maxScoreIdx:" + maxScoreIdx + "  secondMaxScoreIdx:" + secondMaxIdx);
            String formattedScore = String.format("%.3f", maxScore);
            String answer = clsClass.IMAGENET_CLASSES[maxScoreIdx] + formattedScore;
//            formattedScore = String.format("%.3f", secondMaxScore);
//            answer +=  "\n" + clsClass.IMAGENET_CLASSES[secondMaxIdx] + formattedScore;
//            String className = clsClass.IMAGENET_CLASSES[maxScoreIdx];
            textView.setText(answer);



//            // 设置阈值  // 太小了就不要了
//            if (maxScore < threshold) {
//                textView.setText("未训练");
//            } else {
//                String className = clsClass.IMAGENET_CLASSES[maxScoreIdx];
//                String answer = className + maxScore;
//                textView.setText(answer);
//            }

        }
        else{
            Toast.makeText(this, String.valueOf("请选择图片"), Toast.LENGTH_SHORT).show();
        }
    }

    // softmax函数
    public float[] softmax(float[] scores) {
        float max = scores[0];
        for (float score : scores) {
            if (score > max) {
                max = score;
            }
        }

        float sum = 0.0f;
        for (int i = 0; i < scores.length; i++) {
            scores[i] = (float)Math.exp(scores[i] - max);
            sum += scores[i];
        }

        for (int i = 0; i < scores.length; i++) {
            scores[i] /= sum;
        }

        return scores;
    }

    public void shootImage() throws IOException {
        // 创建用于存储照片的文件
        File imageFile = File.createTempFile("image", ".jpg", getExternalFilesDir(null));
        imageUri = FileProvider.getUriForFile(this, "com.example.mycls.fileprovider", imageFile);

        // 创建用于拍摄照片的Intent
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
            startActivityForResult(takePictureIntent, SHOOT_IMAGE_REQUEST);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode == PICK_IMAGE_REQUEST && data != null){
            try {
                bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), data.getData());
                imageview.setImageBitmap(bitmap);
                bitmap = scaleBitmap(bitmap, 300, 300);
                textView.setText("已选择");
                hasImage = 1;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        else if(requestCode == SHOOT_IMAGE_REQUEST && resultCode == RESULT_OK){
            try {
                InputStream is = getContentResolver().openInputStream(imageUri);
                bitmap = BitmapFactory.decodeStream(is);
                imageview.setImageBitmap(bitmap);
                bitmap = scaleBitmap(bitmap, 300, 300);
                textView.setText("已选择");
                hasImage = 1;
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
    }

    public Bitmap scaleBitmap(Bitmap bitmap, int newWidth, int newHeight) {
        // 缩放之后中心裁剪224*224
        bitmap =  Bitmap.createScaledBitmap(bitmap, newWidth, newHeight, true);
        int startX = (bitmap.getWidth() - 224) / 2;
        int startY = (bitmap.getHeight() - 224) / 2;
        bitmap = Bitmap.createBitmap(bitmap, startX, startY, 224, 224);
        return bitmap;

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NotNull String[] permissions, @NotNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                try {
                    shootImage();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            } else {
                // 用户拒绝了权限，你可以在这里解释为什么你的应用需要这个权限，并提供一个重新请求权限的机会。
                Toast.makeText(this, String.valueOf("我要权限"), Toast.LENGTH_SHORT).show();
            }
        }
    }

}
