package tech.aiforce.aienginej.prediction;

public class Period {

	long start; // inclusive
	long end; // exclusive
	
	public Period next() {
		Period next = new Period();
		next.start = end;
		next.end = end + end - start;
		
		return next;
	}
	
	public long interval() {
		return end - start;
	}
	
}
