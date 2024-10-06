package com.example.stockforecast;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface ForecastService {
    @POST("/forecast")
    Call<ForecastResponse> getForecast(@Body ForecastRequest forecastRequest);
}
