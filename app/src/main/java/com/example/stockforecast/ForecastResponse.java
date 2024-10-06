package com.example.stockforecast;

import java.util.List;

public class ForecastResponse {
    private String stock_code;
    private List<Double> forecasted_demand;

    public String getStockCode() {
        return stock_code;
    }

    public List<Double> getForecastedDemand() {
        return forecasted_demand;
    }

}
