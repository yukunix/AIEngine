package tech.aiforce.aienginej.ta;

import java.awt.Color;
import java.awt.Dimension;
import java.text.SimpleDateFormat;
import java.util.List;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.DateAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.Marker;
import org.jfree.chart.plot.ValueMarker;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.StandardXYItemRenderer;
import org.jfree.data.time.Minute;
import org.jfree.data.time.TimeSeriesCollection;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

import eu.verdelhan.ta4j.Decimal;
import eu.verdelhan.ta4j.Indicator;
import eu.verdelhan.ta4j.Tick;
import eu.verdelhan.ta4j.TimeSeries;
import eu.verdelhan.ta4j.Trade;
import eu.verdelhan.ta4j.indicators.simple.ClosePriceIndicator;

public class AnalysisChart {

	public void drawChart(String strategyName, TimeSeries series, List<Trade> trades, Indicator ...indicators) {
		/**
         * Building chart datasets
         */
        TimeSeriesCollection dataset = new TimeSeriesCollection();
        dataset.addSeries(buildChartTimeSeries(series, new ClosePriceIndicator(series), series.getName()));

        TimeSeriesCollection datasetAxis2 = null;
        if (indicators != null) {
        	datasetAxis2 = new TimeSeriesCollection();
        	datasetAxis2.addSeries(buildChartTimeSeries(series, indicators[0], indicators[0].getClass().getSimpleName()));
       
        	if (indicators.length > 1)
        	for (int i = 1; i < indicators.length; i++) {
        		dataset.addSeries(buildChartTimeSeries(series, indicators[i], indicators[i].getClass().getSimpleName()));
			}
        }
        
        /**
         * Creating the chart
         */
        JFreeChart chart = ChartFactory.createTimeSeriesChart(
        		strategyName, // title
                "Date", // x-axis label
                "Price", // y-axis label
                dataset, // data
                true, // create legend?
                true, // generate tooltips?
                false // generate URLs?
                );
        XYPlot plot = (XYPlot) chart.getPlot();
        DateAxis axis = (DateAxis) plot.getDomainAxis();
        axis.setDateFormatOverride(new SimpleDateFormat("yyy-MM-dd"));

        if (datasetAxis2 != null) {
        	addAxis2(plot, datasetAxis2);
        }
        
        /**
         * Running the strategy and adding the buy and sell signals to plot
         */
        addBuySellSignals(series, trades, plot);

        /**
         * Displaying the chart
         */
        displayChart(chart);
	}
	
	private void addAxis2(XYPlot plot, TimeSeriesCollection dataset) {
        final NumberAxis cashAxis = new NumberAxis("Cash Flow Ratio");
        cashAxis.setAutoRangeIncludesZero(false);
        plot.setRangeAxis(1, cashAxis);
        plot.setDataset(1, dataset);
        plot.mapDatasetToRangeAxis(1, 1);
        final StandardXYItemRenderer cashFlowRenderer = new StandardXYItemRenderer();
        cashFlowRenderer.setSeriesPaint(0, Color.blue);
        plot.setRenderer(1, cashFlowRenderer);
    }
	
	private void addBuySellSignals(TimeSeries series, List<Trade> trades, XYPlot plot) {
        // Adding markers to plot
        for (Trade trade : trades) {
            // Buy signal
            double buySignalTickTime = new Minute(series.getTick(trade.getEntry().getIndex()).getEndTime().toDate()).getFirstMillisecond();
            Marker buyMarker = new ValueMarker(buySignalTickTime);
            buyMarker.setPaint(Color.BLUE);
            buyMarker.setLabel("B");
            plot.addDomainMarker(buyMarker);
            // Sell signal
            double sellSignalTickTime = new Minute(series.getTick(trade.getExit().getIndex()).getEndTime().toDate()).getFirstMillisecond();
            Marker sellMarker = new ValueMarker(sellSignalTickTime);
            sellMarker.setPaint(Color.YELLOW);
            sellMarker.setLabel("S");
            plot.addDomainMarker(sellMarker);
        }
    }
	
	private void displayChart(JFreeChart chart) {
        // Chart panel
        ChartPanel panel = new ChartPanel(chart);
        panel.setFillZoomRectangle(true);
        panel.setMouseWheelEnabled(true);
        panel.setPreferredSize(new Dimension(1024, 400));
        // Application frame
        ApplicationFrame frame = new ApplicationFrame("Buy and sell signals");
        frame.setContentPane(panel);
        frame.pack();
        RefineryUtilities.centerFrameOnScreen(frame);
        frame.setVisible(true);
    }
	
	public org.jfree.data.time.TimeSeries buildChartTimeSeries(TimeSeries tickSeries, Indicator<Decimal> indicator, String name) {
        org.jfree.data.time.TimeSeries chartTimeSeries = new org.jfree.data.time.TimeSeries(name);
        for (int i = 0; i < tickSeries.getTickCount(); i++) {
            Tick tick = tickSeries.getTick(i);
            chartTimeSeries.add(new Minute(tick.getEndTime().toDate()), indicator.getValue(i).toDouble());
        }
        return chartTimeSeries;
    }
	
	
}
