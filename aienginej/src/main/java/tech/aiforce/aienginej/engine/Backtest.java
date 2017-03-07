package tech.aiforce.aienginej.engine;

import tech.aiforce.aienginej.engine.oms.PositionManager;
import tech.aiforce.aienginej.engine.pnl.AccountManager;

public class Backtest {

	private Trader trader;

	public Backtest(Trader trader) {
		this.trader = trader;
	}

	void start() {
		trader.startTrade();
	}

	public static void main(String[] args) {
		try {

			Strategy strategy = new AberrationStrategy();
			PositionManager positionManager = new PositionManager();
			AccountManager accountManager = new AccountManager();
			Trader trader = new Trader(strategy, positionManager, accountManager );

			Backtest backtest = new Backtest(trader);
			backtest.start();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
