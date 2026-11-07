
from langchain_core.tools import tool
from datetime import datetime, timezone, timedelta


@tool
def get_current_date():
    """Get the actual current date and time in India."""

    india_timezone = timezone(timedelta(hours=5, minutes=30))

    india_time = datetime.now(india_timezone)

    return india_time.strftime(
        "%A, %d %B %Y, %I:%M:%S %p"
    )


@tool
def calculate_sum(a: float, b: float):
    """Calculate the sum of two numbers."""

    return a + b

