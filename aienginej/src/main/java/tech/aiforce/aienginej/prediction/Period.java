package tech.aiforce.aienginej.prediction;

public class Period {

	private final long start; // inclusive
	private final long end; // exclusive
	
	public Period(long start, long end) {
		this.start = start;
		this.end = end;
	}
	
	public Period next() {
		Period next = new Period(end + end - start, end);
 		return next;
	}
	
	public long interval() {
		return end - start;
	}
	
}
