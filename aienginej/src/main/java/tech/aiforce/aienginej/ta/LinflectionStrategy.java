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

import eu.verdelhan.ta4j.Decimal;
import eu.verdelhan.ta4j.Rule;
import eu.verdelhan.ta4j.Strategy;
import eu.verdelhan.ta4j.TimeSeries;
import eu.verdelhan.ta4j.TradingRecord;
import eu.verdelhan.ta4j.indicators.oscillators.AroonDownIndicator;
import eu.verdelhan.ta4j.indicators.oscillators.AroonUpIndicator;
import eu.verdelhan.ta4j.indicators.simple.ClosePriceIndicator;
import eu.verdelhan.ta4j.indicators.trackers.SMAIndicator;
import eu.verdelhan.ta4j.trading.rules.CrossedDownIndicatorRule;
import eu.verdelhan.ta4j.trading.rules.CrossedUpIndicatorRule;
import eu.verdelhan.ta4j.trading.rules.StopGainRule;
import eu.verdelhan.ta4j.trading.rules.StopLossRule;

public class LinflectionStrategy {

	/**
	 * 
	 * @param series
	 *            - daily ticks
	 * @return
	 */
	public static Strategy buildStrategy(TimeSeries series) {
		if (series == null) {
			throw new IllegalArgumentException("Series cannot be null");
		}

		ClosePriceIndicator closePrice = new ClosePriceIndicator(series);

		SMAIndicator shortSma = new SMAIndicator(closePrice, 20);
		SMAIndicator longSma = new SMAIndicator(closePrice, 120);
		AroonUpIndicator aroonUp = new AroonUpIndicator(series, 25);
		AroonDownIndicator aroonDown = new AroonDownIndicator(series, 25);

		
		// Buying rules:
		// SMA-20 crosses up SMA-120
		// and close price has been mostly down or flat in last 60 days
		Rule buyingRule = new CrossedUpIndicatorRule(shortSma, longSma);
//				.and(new OverIndicatorRule(aroonUp, Decimal.valueOf("70")))
//				.and(new UnderIndicatorRule(aroonDown, Decimal.valueOf("30")));

		// Selling rules:
		// SMA-20 crosses down SMA-120
		// and close price has been mostly up or flat in last 60 days
		Rule sellingRule = new CrossedDownIndicatorRule(shortSma, longSma)
//				.and(new OverIndicatorRule(aroonDown, Decimal.valueOf("70")))
//				.and(new UnderIndicatorRule(aroonUp, Decimal.valueOf("30")))
				.or(new StopGainRule(closePrice, Decimal.valueOf("30")))
				.or(new StopLossRule(closePrice, Decimal.valueOf("10")));

		Strategy strategy = new Strategy(buyingRule, sellingRule);

		return strategy;
	}

	public static void main(String[] args) {

		// Getting a time series (from any provider: CSV, web service, etc.)
//		TimeSeries series = CsvTradesLoader.loadBitstampSeries();
		TimeSeries series = CsvOHLCVLoader.loadSSECSeries();
		System.out.println("Tick count: " + series.getTickCount());

		Strategy strategy = buildStrategy(series);

		TradingRecord tradingRecord = series.run(strategy);

		ResultAnalysisUtil.printResult(series, tradingRecord);

	}
	
}
