package tech.aiforce.aienginej.engine.util;

import java.time.LocalDateTime;

public class DailyPeriod {

	Period nextPeriod;
	
	LocalDateTime start;
	
	public DailyPeriod(LocalDateTime start) {
		this.start = start;
		LocalDateTime end = start.plusDays(1);
		nextPeriod = new Period(start, end);
	}
	
	public Period nextPeriod() {
		// TODO Auto-generated method stub
		return null;
	}

}
