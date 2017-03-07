package tech.aiforce.aienginej.engine.algo;

import tech.aiforce.aienginej.engine.market.Market;
import tech.aiforce.aienginej.engine.oms.Position;
import tech.aiforce.aienginej.engine.pnl.Account;

public interface Algorithm {
	
	Decision analyse(Market market, Position position, Account account);

}
