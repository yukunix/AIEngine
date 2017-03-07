package tech.aiforce.aienginej.engine;

import tech.aiforce.aienginej.engine.algo.Algorithm;
import tech.aiforce.aienginej.engine.algo.Decision;
import tech.aiforce.aienginej.engine.execution.Execution;
import tech.aiforce.aienginej.engine.execution.Executor;
import tech.aiforce.aienginej.engine.market.Market;
import tech.aiforce.aienginej.engine.market.MarketDataFeed;
import tech.aiforce.aienginej.engine.oms.Position;
import tech.aiforce.aienginej.engine.oms.PositionManager;
import tech.aiforce.aienginej.engine.pnl.Account;
import tech.aiforce.aienginej.engine.pnl.AccountManager;

public class Trader {

	Algorithm algorithm;
	
	PositionManager positionManager;
	
	Executor executor;
	
	MarketDataFeed marketDataFeed;
	
	AccountManager accountManager;
	
	public Trader(Strategy strategy, PositionManager positionManager, AccountManager accountManager) {
		executor = strategy.getExecutor();
		algorithm = strategy.getAlgorithm();
		marketDataFeed = strategy.getMarketDataFeed();
		this.accountManager = accountManager;
		this.positionManager = positionManager;
	}
	
	public void startTrade() {
		
		Market market = marketDataFeed.nextMarketDate();
		while (market != null) {
			String sym = market.getSym();
			Position position = positionManager.get(sym);
			Account account = accountManager.getAccount(sym);
			
			Decision decision = algorithm.analyse(market, position, account);
			
			Execution execution = executor.execute(decision);
			
			positionManager.add(execution);
			
			market = marketDataFeed.nextMarketDate();
		}
		
	}

}
