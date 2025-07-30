from AlgorithmImports import *
import numpy as np 


class Algorithm(QCAlgorithm):

    def Initialize(self):
        self.SetCash(100000)
        self.SetStartDate(2017, 9, 1)
        self.SetEndDate(2023, 9, 1)

        # Use an ETF or available symbol on QC if "NIFTY" isn't available
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.lookback = 20
        self.ceiling, self.floor = 30, 10

        self.initialStopRisk = 0.98
        self.trailingStopRisk = 0.9

        self.stopMarketTicket = None
        self.breakoutlvl = 0
        self.highestPrice = 0

        self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                         self.TimeRules.AfterMarketOpen(self.symbol, 20),
                         self.EveryMarketOpen)

    def OnData(self, data):
        self.Plot("Data Chart", self.symbol.Value, self.Securities[self.symbol].Price)

        if self.Portfolio[self.symbol].Invested and self.stopMarketTicket is not None:
            # Plot the current stop price
            self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))

    def EveryMarketOpen(self):
        history = self.History(self.symbol, 31, Resolution.Daily)
        if history.empty or len(history) < 31:
            return

        close = history["close"]
        high = history["high"]

        todayvol = np.std(close[1:31])
        yesterdayvol = np.std(close[0:30])
        deltavol = (todayvol - yesterdayvol) / todayvol

        self.lookback = round(self.lookback * (1 + deltavol))
        self.lookback = max(min(self.lookback, self.ceiling), self.floor)

        recentHighs = self.History(self.symbol, self.lookback, Resolution.Daily)["high"]
        if recentHighs.empty or len(recentHighs) < self.lookback:
            return

        maxHigh = max(recentHighs[:-1])

        # Entry Condition
        if not self.Portfolio[self.symbol].Invested and self.Securities[self.symbol].Close >= maxHigh:
            self.SetHoldings(self.symbol, 1)
            self.breakoutlvl = maxHigh
            self.highestPrice = self.breakoutlvl

            stopPrice = self.initialStopRisk * self.breakoutlvl
            quantity = self.Portfolio[self.symbol].Quantity
            self.stopMarketTicket = self.StopMarketOrder(self.symbol, -quantity, stopPrice)

        # Stop update
        if self.Portfolio[self.symbol].Invested and self.stopMarketTicket is not None:
            currentPrice = self.Securities[self.symbol].Close

            if (currentPrice > self.highestPrice and
                self.initialStopRisk * self.breakoutlvl < currentPrice * self.trailingStopRisk):

                self.highestPrice = currentPrice
                newStopPrice = currentPrice * self.trailingStopRisk

                updateFields = UpdateOrderFields()
                updateFields.StopPrice = newStopPrice
                updateFields.Tag = f"Updated Stop Price to {round(newStopPrice, 2)}"

                self.stopMarketTicket.Update(updateFields)
                self.Debug(updateFields.Tag)
