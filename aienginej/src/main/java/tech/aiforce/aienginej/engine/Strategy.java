package tech.aiforce.aienginej.engine;

import tech.aiforce.aienginej.engine.algo.Algorithm;
import tech.aiforce.aienginej.engine.execution.Executor;
import tech.aiforce.aienginej.engine.market.MarketDataFeed;

public interface Strategy {

	MarketDataFeed getMarketDataFeed();
	
	Executor getExecutor();
	
	Algorithm getAlgorithm();
}
