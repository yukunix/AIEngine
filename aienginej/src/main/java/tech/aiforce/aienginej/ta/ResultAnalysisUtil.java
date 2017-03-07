package tech.aiforce.aienginej.ta;

import eu.verdelhan.ta4j.AnalysisCriterion;
import eu.verdelhan.ta4j.TimeSeries;
import eu.verdelhan.ta4j.TradingRecord;
import eu.verdelhan.ta4j.analysis.CashFlow;
import eu.verdelhan.ta4j.analysis.criteria.AverageProfitableTradesCriterion;
import eu.verdelhan.ta4j.analysis.criteria.RewardRiskRatioCriterion;
import eu.verdelhan.ta4j.analysis.criteria.TotalProfitCriterion;
import eu.verdelhan.ta4j.analysis.criteria.VersusBuyAndHoldCriterion;

public class ResultAnalysisUtil {

	public static void printResult(TimeSeries series, TradingRecord tradingRecord) {
		System.out.println("Tick count: " + series.getTickCount());
		System.out.println("Number of trades for our strategy: " + tradingRecord.getTradeCount());

		// Getting the cash flow of the resulting trades
		CashFlow cashFlow = new CashFlow(series, tradingRecord);

		// Getting the profitable trades ratio
		AnalysisCriterion profitTradesRatio = new AverageProfitableTradesCriterion();
		System.out.println("Profitable trades ratio: " + profitTradesRatio.calculate(series, tradingRecord));
		// Getting the reward-risk ratio
		AnalysisCriterion rewardRiskRatio = new RewardRiskRatioCriterion();
		System.out.println("Reward-risk ratio: " + rewardRiskRatio.calculate(series, tradingRecord));

		// Total profit of our strategy
		// vs total profit of a buy-and-hold strategy
		AnalysisCriterion vsBuyAndHold = new VersusBuyAndHoldCriterion(new TotalProfitCriterion());
		System.out.println("Our profit vs buy-and-hold profit: " + vsBuyAndHold.calculate(series, tradingRecord));

		TotalProfitCriterion totalProfile = new TotalProfitCriterion();
		System.out.println("Total Profit: " + totalProfile.calculate(series, tradingRecord));
	}
	
}
