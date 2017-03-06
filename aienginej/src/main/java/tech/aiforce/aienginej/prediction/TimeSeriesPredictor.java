package tech.aiforce.aienginej.prediction;

public interface TimeSeriesPredictor {
	
	PeriodPrice predict(TimeSeriesPrices timeseries);

}
