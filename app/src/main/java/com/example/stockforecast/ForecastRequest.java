package com.example.stockforecast;

import java.util.List;

public class ForecastRequest {
    private String StockCode;
    private int weeks;

    public ForecastRequest(String product_id, int weeks) {
        this.StockCode = product_id;
        this.weeks = weeks;
    }


}
