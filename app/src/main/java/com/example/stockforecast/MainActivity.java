package com.example.stockforecast;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;


import com.example.stockforecast.ForecastRequest;
import com.example.stockforecast.ForecastResponse;
import com.example.stockforecast.ForecastService;
import com.example.stockforecast.R;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class MainActivity extends AppCompatActivity {

    private EditText stockCodeInput, weeksInput;
    private TextView resultView;
    private Button forecastButton;

    private ForecastService forecastService;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        stockCodeInput = findViewById(R.id.stockCodeInput);
        weeksInput = findViewById(R.id.weeksInput);
        resultView = findViewById(R.id.resultView);
        forecastButton = findViewById(R.id.forecastButton);

        // Setup Retrofit
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.29.237:5000") // Replace with your Flask API's IP address
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        forecastService = retrofit.create(ForecastService.class);

        forecastButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String stockCode = stockCodeInput.getText().toString();
                int weeks = Integer.parseInt(weeksInput.getText().toString());

                makeForecastRequest(stockCode, weeks);
            }
        });
    }

    private void makeForecastRequest(String stockCode, int weeks) {
        ForecastRequest request = new ForecastRequest(stockCode, weeks);

        forecastService.getForecast(request).enqueue(new Callback<ForecastResponse>() {
            @Override
            public void onResponse(Call<ForecastResponse> call, Response<ForecastResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    ForecastResponse forecastResponse = response.body();
                    resultView.setText(forecastResponse.getForecastedDemand().toString());
                } else {
                    Toast.makeText(MainActivity.this, "API call failed", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ForecastResponse> call, Throwable t) {
                Toast.makeText(MainActivity.this, "Failed to communicate with API", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
