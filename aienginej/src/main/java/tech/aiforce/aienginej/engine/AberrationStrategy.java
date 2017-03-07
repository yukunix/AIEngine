package tech.aiforce.aienginej.engine;

import tech.aiforce.aienginej.engine.algo.AberrationAlgorithm;
import tech.aiforce.aienginej.engine.algo.Algorithm;
import tech.aiforce.aienginej.engine.execution.Executor;
import tech.aiforce.aienginej.engine.execution.MockExecutor;
import tech.aiforce.aienginej.engine.market.DailyMarketDataFeed;
import tech.aiforce.aienginej.engine.market.MarketDataFeed;

public class AberrationStrategy implements Strategy {

	public MarketDataFeed getMarketDataFeed() {
		return new DailyMarketDataFeed();
	}

	public Executor getExecutor() {
		return new MockExecutor();
	}

	public Algorithm getAlgorithm() {
		return new AberrationAlgorithm();
	}

}
