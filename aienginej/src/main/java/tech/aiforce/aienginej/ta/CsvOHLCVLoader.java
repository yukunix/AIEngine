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

import au.com.bytecode.opencsv.CSVReader;
import eu.verdelhan.ta4j.TimeSeries;
import eu.verdelhan.ta4j.Tick;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.joda.time.DateTime;

/**
 * This class build a Ta4j time series from a CSV file containing ticks.
 */
public class CsvOHLCVLoader {

    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd");

    /**
     * @return a time series from Apple Inc. ticks.
     */
    public static TimeSeries loadAppleIncSeries() {
    	InputStream stream = CsvOHLCVLoader.class.getClassLoader().getResourceAsStream("appleinc_ticks_from_20130101_usd.csv");
    	return loadTimeSeries(stream, "apple_ticks", false);
    }
    
    /**
     * @return Shanghai Stock Exchange Composite index from 1997 to 2016
     */
    public static TimeSeries loadSSECSeries() {
    	InputStream stream = CsvOHLCVLoader.class.getClassLoader().getResourceAsStream("YAHOO-INDEX_SSEC.csv");
    	return loadTimeSeries(stream, "ssec_ticks", true);
    }
    
    public static TimeSeries loadTimeSeries(InputStream stream, String name, boolean reverse) {
        List<Tick> ticks = new ArrayList<Tick>();

        CSVReader csvReader = new CSVReader(new InputStreamReader(stream, Charset.forName("UTF-8")), ',', '"', 1);
        try {
            String[] line;
            while ((line = csvReader.readNext()) != null) {
                DateTime date = new DateTime(DATE_FORMAT.parse(line[0]));
                double open = Double.parseDouble(line[1]);
                double high = Double.parseDouble(line[2]);
                double low = Double.parseDouble(line[3]);
                double close = Double.parseDouble(line[4]);
                double volume = Double.parseDouble(line[5]);

                ticks.add(new Tick(date, open, high, low, close, volume));
            }
        } catch (IOException ioe) {
            Logger.getLogger(CsvOHLCVLoader.class.getName()).log(Level.SEVERE, "Unable to load ticks from CSV", ioe);
        } catch (ParseException pe) {
            Logger.getLogger(CsvOHLCVLoader.class.getName()).log(Level.SEVERE, "Error while parsing date", pe);
        } catch (NumberFormatException nfe) {
            Logger.getLogger(CsvOHLCVLoader.class.getName()).log(Level.SEVERE, "Error while parsing value", nfe);
        }

        if (reverse) {
        	Collections.reverse(ticks);
        }
        
        return new TimeSeries(name, ticks);
    }

    public static void main(String[] args) {
//        TimeSeries series = CsvOHLCVLoader.loadAppleIncSeries();
        TimeSeries series = CsvOHLCVLoader.loadSSECSeries();
        
        System.out.println("Series: " + series.getName() + " (" + series.getSeriesPeriodDescription() + ")");
        System.out.println("Number of ticks: " + series.getTickCount());
        System.out.println("First tick: \n"
                + "\tVolume: " + series.getTick(0).getVolume() + "\n"
                + "\tOpen price: " + series.getTick(0).getOpenPrice()+ "\n"
                + "\tClose price: " + series.getTick(0).getClosePrice());
    }
}
