package cse403.finderskeepers;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.ParcelFileDescriptor;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.FileDescriptor;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import cse403.finderskeepers.data.UserInfoHolder;
import okhttp3.MediaType;
import okhttp3.RequestBody;

/**
 * Created by Jared on 11/8/2016.
 */

public class AddItemWindowActivity extends AppCompatActivity {

    private int GET_IMAGE = 1;
    private static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");
    private boolean imageSet;

    // Item info

    // Is item being edited: true = being edited, false = being created
    private boolean edit;

    // id of item, if edited
    private int itemId;

    // tags of item, if edited
    private String tags;

    // image of item, if being edited
    private Bitmap image;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getIntent().getExtras() != null && getIntent().getExtras().containsKey("ITEM_ID") && getIntent().getExtras().containsKey("TAGS")) {
            this.itemId = getIntent().getExtras().getInt("ITEM_ID");
            this.tags = getIntent().getExtras().getString("TAGS");
            this.image = (Bitmap) getIntent().getExtras().get("IMAGE");

            // Change text of add item button if item info exists
            Button addItemButton = (Button) findViewById(R.id.upload_button);
            addItemButton.setText("Update Item");
            this.edit = true;
        } else {
            this.itemId = 0;
            this.edit = false;
        }
        imageSet = false;
        setContentView(R.layout.content_additem_page);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        ImageButton addItem = (ImageButton) findViewById(R.id.add_item_img);
        Button upload = (Button) findViewById(R.id.upload_button);
        upload.setOnClickListener(this.uploadItemListener);
        addItem.setOnClickListener(this.itemPicListener);
    }

    private View.OnClickListener uploadItemListener = new View.OnClickListener() {
        @Override
        public void onClick(View view){
            if (!imageSet) {
                return;
            }
            EditText tags = (EditText) findViewById(R.id.editTags);
            Scanner scanner = new Scanner(tags.getText().toString());

            // create tags array
            JSONArray jsonTags = new JSONArray();
            while(scanner.hasNext()) {
                jsonTags.put(scanner.next());
            }

            // encode the current image as base64 JPEG
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            ImageButton addItem = (ImageButton) findViewById(R.id.add_item_img);
            Drawable drawable = addItem.getDrawable();
            Bitmap image = ((BitmapDrawable) drawable).getBitmap();
            image.compress(Bitmap.CompressFormat.JPEG, 100, stream);
            byte[] imageBytes = stream.toByteArray();
            String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);

            // create request JSON
            JSONObject requestJSON = new JSONObject();
            try {
                requestJSON.put("tags", jsonTags);
                requestJSON.put("user_id", UserInfoHolder.getInstance().getUID());
                requestJSON.put("item_image_data", encodedImage);
            } catch (JSONException e) {
                e.printStackTrace();
                return;
            }

            RequestBody requestBody = RequestBody.create(JSON, requestJSON.toString());

            finish();
        }
    };

    //Listener for item add buttons
    private View.OnClickListener itemPicListener = new View.OnClickListener() {
        @Override
        public void onClick(View view){
            Intent getImageIntent = new Intent();
            getImageIntent.setType("image/*");
            getImageIntent.setAction(Intent.ACTION_GET_CONTENT);
            startActivityForResult(Intent.createChooser(getImageIntent, "Select Image for Item"), GET_IMAGE);
        }
    };

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode == GET_IMAGE && resultCode == Activity.RESULT_OK) {
            Uri selectedImage = data.getData();
            ParcelFileDescriptor parcelFileDescriptor;
            try {
                parcelFileDescriptor = getContentResolver().openFileDescriptor(selectedImage, "r");
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }

            // error getting file descriptor
            if (parcelFileDescriptor == null) {
                return;
            }

            FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();
            Bitmap item = BitmapFactory.decodeFileDescriptor(fileDescriptor);
            try {
                parcelFileDescriptor.close();
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }

            ImageView img = (ImageView) findViewById(R.id.add_item_img);
            img.setImageBitmap(item);
            imageSet = true;
        }
    }
}
