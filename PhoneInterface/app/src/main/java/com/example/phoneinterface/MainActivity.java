package com.example.phoneinterface;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private EditText editText;
    private LinearLayout linearLayout;
    private ScrollView scrollView;
    private Button buttonShowProducts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        /* initialize view */
        editText = findViewById(R.id.editText);             // text in typing place
        Button sendButton = findViewById(R.id.sendButton);
        linearLayout = findViewById(R.id.linearLayout);
        scrollView = findViewById(R.id.scrollView);

        /*
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });*/


        buttonShowProducts = findViewById(R.id.button_show_products);
        buttonShowProducts.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showProductsDialog();
            }
        });


        // button to send message from typing place
        sendButton.setOnClickListener(v -> {
            String message = editText.getText().toString().trim();
            if (!message.isEmpty()) {
                addMessageToChat("You: " + message, true);

                // 构建请求的JSON数据
                JSONObject postData = new JSONObject();
                try {
                    postData.put("message", message);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                /*
                // build JSON request part
                MediaType JSON = MediaType.parse("application/json; charset=utf-8");
                RequestBody body = RequestBody.create(postData.toString(), JSON);

                // build part interact with backend LLM：
                // asynchronously send POST request to Flask server
                OkHttpClient client = new OkHttpClient();
                // cannot use localhost directly, otherwise it would try to connect to VM itself instead of computer;
                // use the IPv4 in LAN
                String url = "http://"+"10.0.2.2"+":5000/chat";

                Request request = new Request.Builder()
                        .url(url)
                        .post(body)
                        .build();

                // send request
                client.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onFailure(Call call, IOException e) {
                        e.printStackTrace();
                    }

                    @Override
                    public void onResponse(Call call, Response response) throws IOException {
                        if (response.isSuccessful()) {
                            final String responseBody = response.body().string();
                            // use a simple JSON extraction method to get reply
                            try {
                                JSONObject jsonObject = new JSONObject(responseBody);
                                final String reply = jsonObject.getString("reply");
                                // update screen in UI thread, show content of reply
                                runOnUiThread(() -> {
                                    addMessageToChat("Bot: " + reply, false);
                                });
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    }
                });*/


                new Thread(() -> {
                    try {
                        // get InetAddress instance
                        //InetAddress inetAddress = InetAddress.getLocalHost();
                        //String hostAddress = ""+inetAddress.getHostAddress();
                        //Socket socket = new Socket(hostAddress, 5001);
                        //Socket socket = new Socket("10.0.2.2", 5001);
                        //Socket socket = new Socket("192.168.43.243", 5001);
                        Socket socket = new Socket("10.129.99.20", 5001);  // link to local server: BUPT-portal
                        PrintWriter out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);
                        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                        out.println(message);  // send message
                        String reply = in.readLine();  // read reply
                        runOnUiThread(() -> addMessageToChat("Bot: " + reply, false));

                        socket.close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }).start();

                //addMessageToChat("Bot: Yes", false);
                editText.setText("");
                scrollView.post(() -> scrollView.fullScroll(ScrollView.FOCUS_DOWN));
            }
        });
    }

    private void showProductsDialog() {
        LayoutInflater inflater = LayoutInflater.from(this);
        View dialogView = inflater.inflate(R.layout.dialog_products, null);
        TableLayout table = dialogView.findViewById(R.id.productsTable);

        // array: name, kind, amount
        String[][] products = {
                {"Funds", "", ""},
                {"Ping An Currency Fund A", "Currency Fund", "12000"},
                {"Guang Da Currency Fund B", "Currency Fund", "16500"},
                {"Zhao Shang Currency Fund C", "Currency Fund", "20000"},
                {"Gong Shang Stock Fund A", "Stock Fund", "59000"},
                {"Nong Ye Stock Fund B", "Stock Fund", "64000"},
                {"Guang Da Stock Fund C", "Stock Fund", "70000"},
                {"Insurances", "", ""},
                {"Gong Shang Medical Insurance A", "Medical Insurance", "35000"},
                {"Zhong Xin Medical Insurance B", "Medical Insurance", "39000"},
                {"Ping An Medical Insurance C", "Medical Insurance", "44000"},
                {"Hua Xia Accidental Insurance A", "Accidental Insurance", "36000"},
                {"Jian She Accidental Insurance B", "Accidental Insurance", "39000"},
                {"Nong Ye Accidental Insurance C", "Accidental Insurance", "42000"},
                {"Debenture", "", ""},
                {"Xing Ye Debenture A", "Debenture", "80000"},
                {"Chong Qing Debenture B", "Debenture", "84000"},
                {"Zhong Xin Debenture C", "Debenture", "89000"},
        };

        for (String[] product : products) {
            TableRow row = new TableRow(this);
            for (String field : product) {
                TextView textView = new TextView(this);
                textView.setText(field);
                textView.setPadding(8, 8, 8, 8);
                TableRow.LayoutParams params = new TableRow.LayoutParams(TableRow.LayoutParams.WRAP_CONTENT, TableRow.LayoutParams.WRAP_CONTENT);
                params.setMargins(0, 0, 20, 0); // right margin
                textView.setLayoutParams(params);
                row.addView(textView);
            }
            table.addView(row, new TableLayout.LayoutParams(TableLayout.LayoutParams.MATCH_PARENT, TableLayout.LayoutParams.WRAP_CONTENT));
        }

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setView(dialogView)
                .setPositiveButton("close", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        dialogInterface.dismiss();
                    }
                })
                .show();
    }
    

    private void addMessageToChat(String message, boolean isUser) {
        // Create a new horizontal LinearLayout for each message
        LinearLayout messageLayout = new LinearLayout(this);
        messageLayout.setOrientation(LinearLayout.HORIZONTAL);
        messageLayout.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));

        ImageView avatar = new ImageView(this);
        TextView textView = new TextView(this);
        textView.setText(message);
        textView.setTextSize(16f);
        LinearLayout.LayoutParams textParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        LinearLayout.LayoutParams imageParams = new LinearLayout.LayoutParams(
                100, 100  // Set the size of the avatar
        );
        imageParams.gravity = Gravity.CENTER_VERTICAL;

        // padding between the avatar and the text
        int drawablePadding = 20;  // spacing
        int marginSize = 12;       // margin between messages

        if (isUser) {
            avatar.setImageResource(R.drawable.matthew); // Ensure you have this resource
            textParams.gravity = Gravity.END;
            textView.setBackgroundResource(R.drawable.user_message_bg);
            messageLayout.setGravity(Gravity.RIGHT); // align to the right
            textView.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.user_message_bg, 0);
            textView.setCompoundDrawablePadding(drawablePadding);
            messageLayout.addView(textView, textParams);
            messageLayout.addView(avatar, imageParams);
        } else {
            avatar.setImageResource(R.drawable.moss);
            textParams.gravity = Gravity.START;
            textView.setBackgroundResource(R.drawable.bot_message_bg);
            messageLayout.setGravity(Gravity.LEFT); // align to the left
            textView.setCompoundDrawablesWithIntrinsicBounds(R.drawable.bot_message_bg, 0, 0, 0);
            textView.setCompoundDrawablePadding(drawablePadding);
            messageLayout.addView(avatar, imageParams);
            messageLayout.addView(textView, textParams);
        }

        // set head
        textParams.setMargins(marginSize, marginSize, marginSize, marginSize);
        textView.setLayoutParams(textParams);
        // pad between head and text
        textView.setPadding(16, 16, 16, 16);
        linearLayout.addView(messageLayout);

        // scroll to the bottom every time a new message is added
        scrollView.post(() -> scrollView.fullScroll(ScrollView.FOCUS_DOWN));
    }

}
