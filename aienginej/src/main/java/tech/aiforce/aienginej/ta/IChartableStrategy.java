package tech.aiforce.aienginej.ta;

import eu.verdelhan.ta4j.Indicator;

public interface IChartableStrategy {
	
	void addIndicator(Indicator indicator);
	
	Indicator[] getIndicators();

}
