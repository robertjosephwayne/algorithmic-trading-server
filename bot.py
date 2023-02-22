from strategies.moving_average_crossover import MovingAverageCrossoverStrategy

moving_average_crossover = MovingAverageCrossoverStrategy(
    sma_fast_hours=79, sma_slow_hours=143, max_allocation=5000
)


async def process_bar(symbol):
    await moving_average_crossover.process_bar(symbol)
