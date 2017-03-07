package tech.aiforce.aienginej.engine.util;

import java.time.LocalDateTime;

public class Period {
	
	private LocalDateTime start;
	private LocalDateTime end;
	
	public Period(LocalDateTime start, LocalDateTime end) {
		this.start = start;
		this.end = end;
	}

	public LocalDateTime getStart() {
		return start;
	}

	public LocalDateTime getEnd() {
		return end;
	}

}