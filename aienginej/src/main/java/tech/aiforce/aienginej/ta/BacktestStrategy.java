/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2014-2016 Marc de Verdelhan & respective authors (see AUTHORS)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package tech.aiforce.aienginej.ta;

import java.util.List;

import eu.verdelhan.ta4j.TimeSeries;
import eu.verdelhan.ta4j.Trade;
import eu.verdelhan.ta4j.TradingRecord;

public class BacktestStrategy {

    public static void main(String[] args) {

        // Getting the time series
        TimeSeries series = CsvOHLCVLoader.loadSSECSeries();

        // Building the trading strategy
        ChartableStrategy rsi2 = RSI2Strategy.buildStrategy(series);
        ChartableStrategy momentum = MovingMomentumStrategy.buildStrategy(series);

        for (ChartableStrategy strategy : new ChartableStrategy[]{rsi2, momentum}) {
        	TradingRecord tradingRecord = series.run(strategy);
        	List<Trade> trades = tradingRecord.getTrades();
        	
        	System.out.println("------------- " + strategy.getName() + " -------------- ");
        	StrategyAnalysis.printResult(series, tradingRecord);
        	System.out.println("------------- end of " + strategy.getName() + " -------------");
        	
        	
        	new AnalysisChart().drawChart(strategy.getName(), series, trades, strategy.getIndicators());
		}
        
    }
}
