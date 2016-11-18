package cse403.finderskeepers;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

import cse403.finderskeepers.data.UserInfoHolder;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Response;

import static android.view.View.GONE;

public class ViewUserTradeActivity extends AppCompatActivity {

    private int tradeID;

    private int theirUID;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_user_trade);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        if(getIntent().getExtras() != null && getIntent().getExtras().containsKey("USERID")){
            tradeID = getIntent().getExtras().getInt("TRADEID");
        }

        Button viewUserButton = (Button) findViewById(R.id.view_profile);
        viewUserButton.setOnClickListener(viewUserListener);

        populatePage();
    }

    /**
     * Listener which opens item viewing window
     */
    private View.OnClickListener viewItemListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            Intent addItemIntent = new Intent(ViewUserTradeActivity.this, OtherUserItemViewActivity.class);
            addItemIntent.putExtra("ITEM_ID", ((AddableItem) view).getItemId());
            addItemIntent.putExtra("TAGS", ((AddableItem) view).getTags());
            startActivity(addItemIntent);
        }
    };

    /**
     * Listener which opens profile of other user
     */
    private View.OnClickListener viewUserListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            Intent viewUserIntent = new Intent(ViewUserTradeActivity.this, OtherUserPageActivity.class);
            viewUserIntent.putExtra("USERID", ((BrowseResultUser) view).getUserId());
            startActivity(viewUserIntent);
        }
    };

    private void populatePage() {
        UserAPIService userapiservice = UserInfoHolder.getInstance().getAPIService();

        Call<ResponseBody> trade = userapiservice.getTrade(tradeID);
        try {
            Response<ResponseBody> tradeCall = trade.execute();
            JSONObject tradeObj = new JSONObject(tradeCall.body().string()).getJSONObject("trade");

            TextView statusString = (TextView) findViewById(R.id.status_string);

            if (!tradeObj.getString("status").equals("T_OPEN") || !(UserInfoHolder.getInstance().getUID() == tradeObj.getInt("recipient_id"))) {
                Button acceptButton = (Button) findViewById(R.id.accept_trade);
                acceptButton.setVisibility(GONE);

                Button rejectButton = (Button) findViewById(R.id.reject_trade);
                rejectButton.setVisibility(GONE);
            }

            if (tradeObj.getString("status").equals("T_OPEN") && UserInfoHolder.getInstance().getUID() == tradeObj.getInt("recipient_id")) {
                statusString.setText("Incoming - Pending");
            } else if (tradeObj.getString("status").equals("T_OPEN")) {
                statusString.setText("Outgoing - Pending");
            } else if (tradeObj.getString("stats").equals("T_COMPLETED")) {
                statusString.setText("Completed");
            } else if (tradeObj.getString("stats").equals("T_REJECTED")) {
                statusString.setText("Rejected");
            }

            JSONArray ourItems;
            JSONArray theirItems;

            if (UserInfoHolder.getInstance().getUID() == tradeObj.getInt("initiator_id")) {
                theirUID = tradeObj.getInt("recipient_id");
                ourItems = tradeObj.getJSONArray("offered_item_ids");
                theirItems = tradeObj.getJSONArray("requested_item_ids");
            } else {
                theirUID = tradeObj.getInt("initiator_id");
                ourItems = tradeObj.getJSONArray("requested_item_ids");
                theirItems = tradeObj.getJSONArray("offered_item_ids");
            }

            LinearLayout ourItemsLayout = (LinearLayout) findViewById(R.id.your_items_list);
            LinearLayout theirItemsLayout = (LinearLayout) findViewById(R.id.their_item_list);

            populateLayoutWithItems(ourItems, ourItemsLayout, viewItemListener);
            populateLayoutWithItems(theirItems, theirItemsLayout, viewItemListener);
        } catch (IOException e) {
            disconnectionError();
            e.printStackTrace();
        } catch (JSONException e) {
            disconnectionError();
            e.printStackTrace();
        }
    }

    private void disconnectionError(){
        Intent intent = new Intent(ViewUserTradeActivity.this, DisconnectionError.class);
        startActivity(intent);
    }

    private void populateLayoutWithItems(JSONArray inventory, LinearLayout layout, View.OnClickListener listener) {
        for (int i = 0; i < inventory.length(); i++) {
            try {
                Call<ResponseBody> getItem = UserInfoHolder.getInstance().getAPIService().getItem(inventory.getInt(i));
                Response<ResponseBody> doGetItemCall = getItem.execute();
                JSONObject item = new JSONObject(doGetItemCall.body().string()).getJSONObject("item");
                Bitmap image;

                URL itemImageURL = new URL(item.getString("image_url"));
                image = BitmapFactory.decodeStream(itemImageURL.openConnection().getInputStream());

                if (image != null) {
                    AddableItem newItem = new AddableItem(this, "", item.getInt("item_id"));
                    LinearLayout.LayoutParams params = new LinearLayout
                            .LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.MATCH_PARENT);
                    newItem.setImageBitmap(image);
                    newItem.setLayoutParams(params);
                    newItem.setAdjustViewBounds(true);
                    newItem.setScaleType(ImageView.ScaleType.FIT_CENTER);
                    newItem.setOnClickListener(listener);
                    layout.addView(newItem, 0);
                }
            } catch (JSONException e) {
                disconnectionError();
                e.printStackTrace();
            } catch (MalformedURLException e) {
                disconnectionError();
                e.printStackTrace();
            } catch (IOException e) {
                disconnectionError();
                e.printStackTrace();
            }

        }
    }
}
