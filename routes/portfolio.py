from fastapi import APIRouter
from connectors.alpaca.rest.client import alpaca_rest_client

router = APIRouter(
    prefix="/api/portfolio"
)


@router.get("/positions")
async def get_positions():
    positions = alpaca_rest_client.list_positions()

    orders = alpaca_rest_client.list_orders()
    stop_loss_orders = filter(lambda order: "stop" in order.type, orders)
    stop_loss_orders = list(stop_loss_orders)

    response = []

    for position in positions:
        stop_loss_order = next((order for order in stop_loss_orders if position.symbol == order.symbol), None)

        response.append({
            "asset_class": position.asset_class,
            "symbol": position.symbol,
            "quantity": position.qty,
            "side": position.side,
            "exchange": position.exchange,
            "cost_basis": position.cost_basis,
            "market_value": position.market_value,
            "average_entry_price": position.avg_entry_price,
            "current_price": position.current_price,
            "stop_price": stop_loss_order.stop_price if stop_loss_order else None,
            "change_today": position.change_today,
            "intraday_unrealized_pl": position.unrealized_intraday_pl,
            "intraday_unrealized_pl_percent": position.unrealized_intraday_plpc,
            "total_unrealized_pl": position.unrealized_pl,
            "total_unrealized_pl_percent": position.unrealized_plpc
        })

    return response


@router.get("/activities")
async def get_activities():
    result = alpaca_rest_client.get_activities()

    response = []

    for activity in result:
        if activity.activity_type == "FILL":
            response.append({
                "activity_type": activity.activity_type,
                "cumulative_quantity": activity.cum_qty,
                "order_status": activity.order_status,
                "price": activity.price,
                "quantity": activity.qty,
                "side": activity.side,
                "symbol": activity.symbol,
                "transaction_time": activity.transaction_time,
                "type": activity.type
            })

    return response


@router.get("/deposits")
async def get_deposits():
    result = alpaca_rest_client.get_activities()

    response = []

    for activity in result:
        if activity.activity_type == "OCT":
            print(activity)
            response.append({
                "activity_type": activity.activity_type,
                "date": activity.date,
                "price": activity.price,
                "quantity": activity.quantity
            })

    return response


@router.get("/orders")
async def get_orders():
    result = alpaca_rest_client.list_orders()

    response = []

    for order in result:
        response.append({
            "symbol": order.symbol,
            "quantity": order.qty,
            "filled_quantity": order.filled_qty,
            "side": order.side,
            "type": order.type,
            "time_in_force": order.time_in_force,
            "limit_price": order.limit_price,
            "stop_price": order.stop_price,
            "notional": order.notional,
            "trail_percent": order.trail_percent,
            "trail_price": order.trail_price
        })

    return response


@router.get("/history")
async def get_history():
    result = alpaca_rest_client.get_portfolio_history(date_start="2023-03-01", timeframe="1D")

    activities = alpaca_rest_client.get_activities()
    daily_deposits = {}

    for activity in activities:
        if activity.activity_type == "OCT":
            price = float(activity.price)
            quantity = float(activity.qty)
            deposit_value = price * quantity

            if activity.date not in daily_deposits.keys():
                daily_deposits.update({activity.date: deposit_value})
            else:
                daily_deposits[activity.date] += deposit_value
        elif activity.activity_type == "CSD":
            deposit_value = float(activity.net_amount)
            if activity.date not in daily_deposits.keys():
                daily_deposits.update({activity.date: deposit_value})
            else:
                daily_deposits[activity.date] += deposit_value

    print(daily_deposits)
    response = []

    for i in range(len(result.equity)):
        response.append({
            "timestamp": result.timestamp[i] * 1000,
            "equity": result.equity[i],
            "pl": result.profit_loss[i],
            "pl_percent": result.profit_loss_pct[i]
        })

    return response