package tech.aiforce.aienginej.ta;

import java.util.ArrayList;
import java.util.List;

import eu.verdelhan.ta4j.Indicator;
import eu.verdelhan.ta4j.Rule;
import eu.verdelhan.ta4j.Strategy;

public class ChartableStrategy extends Strategy implements IChartableStrategy {

	private String name;
    
    private List<Indicator> indicators = new ArrayList<Indicator>();
    
    public ChartableStrategy(Rule entryRule, Rule exitRule, String name) {
    	super(entryRule, exitRule);
    	this.name = name;
    }
    
    public String getName() {
		return name;
	}
    
    public void addIndicator(Indicator indicator) {
    	indicators.add(indicator);
    }
    
	@Override
	public Indicator[] getIndicators() {
		return indicators.toArray(new Indicator[0]);
	}

}
