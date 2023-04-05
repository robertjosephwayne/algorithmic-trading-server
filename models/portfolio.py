from datetime import datetime
from connectors.alpaca.rest.client import alpaca_rest_client
from connectors.tradier.rest.client import tradier_rest_client
import pandas as pd


class Portfolio:
    @staticmethod
    async def get_positions():
        positions = tradier_rest_client.get_positions()

        formatted_positions = []

        for position in positions:
            formatted_positions.append({
                "symbol": position.symbol,
                "quantity": position.quantity,
                "cost_basis": position.cost_basis,
                "date_acquired": position.date_acquired
            })

        return formatted_positions

    @staticmethod
    async def get_activities():
        history = tradier_rest_client.get_history(type="trade")
        print(history)

        formatted_activities = []

        for event in history:
            if event.activity_type == "trade":
                formatted_activities.append({
                    "price": event.trade.price,
                    "quantity": event.trade.quantity,
                    "symbol": event.trade.symbol,
                    "transaction_time": event.date,
                    "type": event.type
                })

        return formatted_activities

    @staticmethod
    async def get_deposits():
        activities = alpaca_rest_client.get_activities()

        deposits = []

        for activity in activities:
            if activity.activity_type == "OCT":
                deposits.append({
                    "activity_type": activity.activity_type,
                    "date": activity.date,
                    "price": activity.price,
                    "quantity": activity.quantity
                })

        return deposits

    @staticmethod
    async def get_orders():
        orders = tradier_rest_client.get_orders()

        formatted_orders = []

        for order in orders:
            formatted_orders.append({
                "symbol": order.symbol,
                "quantity": order.quantity,
                "side": order.side,
                "type": order.type,
                "time_in_force": order.duration,
                "limit_price": order.price,
            })

        return formatted_orders

    @staticmethod
    async def get_history():
        result = alpaca_rest_client.get_portfolio_history(date_start="2023-03-08", timeframe="1D")

        activities = alpaca_rest_client.get_activities()
        daily_net_deposits_df = pd.DataFrame(columns=['activity_date', 'deposit_value'])

        for activity in activities:
            if activity.activity_type == "OCT":
                price = float(activity.price)
                quantity = float(activity.qty)
                deposit_value = price * quantity

                existing_deposit_index = daily_net_deposits_df.index[
                    daily_net_deposits_df['activity_date'] == activity.date].tolist()

                if not len(existing_deposit_index):
                    daily_net_deposits_df = pd.concat(objs=[daily_net_deposits_df, pd.DataFrame({
                        "activity_date": [activity.date],
                        "deposit_value": [deposit_value]
                    })], ignore_index=True)
                else:
                    daily_net_deposits_df.loc[existing_deposit_index[0], ['deposit_value']] += deposit_value

            elif activity.activity_type == "CSD":
                deposit_value = float(activity.net_amount)

                existing_deposit_index = daily_net_deposits_df.index[
                    daily_net_deposits_df['activity_date'] == activity.date].tolist()

                if not len(existing_deposit_index):
                    daily_net_deposits_df = pd.concat(objs=[daily_net_deposits_df, pd.DataFrame({
                        "activity_date": [activity.date],
                        "deposit_value": [deposit_value]
                    })], ignore_index=True)
                else:
                    daily_net_deposits_df.loc[existing_deposit_index[0], ['deposit_value']] += deposit_value

            elif activity.activity_type == "CSW":
                withdrawal_value = -float(activity.net_amount)

                existing_deposit_index = daily_net_deposits_df.index[
                    daily_net_deposits_df['activity_date'] == activity.date].tolist()

                if not len(existing_deposit_index):
                    daily_net_deposits_df = pd.concat(objs=[daily_net_deposits_df, pd.DataFrame({
                        "activity_date": [activity.date],
                        "deposit_value": [withdrawal_value]
                    })], ignore_index=True)
                else:
                    daily_net_deposits_df.loc[existing_deposit_index[0], ['deposit_value']] += withdrawal_value

        for i in range(len(result.equity)):
            date = datetime.fromtimestamp(result.timestamp[i - 1])
            formatted_date = date.strftime("%Y-%m-%d")

            existing_activity_index = daily_net_deposits_df.index[
                daily_net_deposits_df['activity_date'] == formatted_date].tolist()

            if not len(existing_activity_index):
                daily_net_deposits_df = pd.concat(objs=[daily_net_deposits_df, pd.DataFrame({
                    "activity_date": [formatted_date],
                    "equity": [result.equity[i]]
                })], ignore_index=True)
            else:
                daily_net_deposits_df.loc[existing_activity_index[0], ['equity']] = [result.equity[i]]

        daily_net_deposits_df.sort_values(by='activity_date', inplace=True, ignore_index=True)
        daily_net_deposits_df.fillna(0, inplace=True)

        cumulative_pl = 0
        base_equity = None
        for index, row in daily_net_deposits_df.iterrows():
            if index == 0:
                base_equity = row.equity
            else:
                previous_equity = daily_net_deposits_df.loc[[index - 1], 'equity']

                if previous_equity.item() == 0 or row.equity == 0:
                    continue

                daily_pl = row.equity - previous_equity - row.deposit_value
                daily_pl_percent = daily_pl / previous_equity

                cumulative_pl = daily_pl
                cumulative_pl_percent = cumulative_pl / base_equity

                average_daily_pl_percent = cumulative_pl_percent / index

                trading_days_per_year = 252
                annualized_pl_percent = (1 + average_daily_pl_percent) ** trading_days_per_year - 1

                daily_net_deposits_df.loc[[index], ['daily_pl']] = [daily_pl]
                daily_net_deposits_df.loc[[index], ['daily_pl_percent']] = [daily_pl_percent]
                daily_net_deposits_df.loc[[index], ['cumulative_pl']] = [cumulative_pl]
                daily_net_deposits_df.loc[[index], ['cumulative_pl_percent']] = [cumulative_pl_percent]
                daily_net_deposits_df.loc[[index], ['average_daily_pl_percent']] = [average_daily_pl_percent]
                daily_net_deposits_df.loc[[index], ['annualized_pl_percent']] = [annualized_pl_percent]

        daily_net_deposits_df.fillna(0, inplace=True)

        formatted_history = []

        for index, row in daily_net_deposits_df.iterrows():
            formatted_history.append({
                "timestamp": row.activity_date,
                "equity": row.equity,
                "daily_pl": row.daily_pl,
                "daily_pl_percent": row.daily_pl_percent,
                "daily_net_deposits": row.deposit_value,
                "cumulative_pl": row.cumulative_pl,
                "cumulative_pl_percent": row.cumulative_pl_percent,
                "average_daily_pl_percent": row.average_daily_pl_percent,
                "annualized_pl_percent": row.annualized_pl_percent,
            })

        return formatted_history
