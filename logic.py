# logic.py
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class CalculationError(Exception):
    """Custom exception for tip calculation errors."""
    pass


def calculate_tip_per_person(bill_str: str, people_str: str, tip_percent: int) -> Decimal:
    """
    bill_str: total bill as string (e.g. "125.50")
    people_str: number of people as string (e.g. "2")
    tip_percent: tip percentage as int (0–100)
    """
    # Parse bill
    try:
        bill = Decimal(bill_str.strip())
    except InvalidOperation:
        raise CalculationError("Please enter a valid number (e.g. 123.45).")

    if bill <= 0:
        raise CalculationError("Bill must be positive.")

    # Parse people
    try:
        people = int(people_str.strip())
    except ValueError:
        raise CalculationError("Please enter a valid integer for number of people.")

    if people <= 0:
        raise CalculationError("People must be positive.")

    # Calculate tip
    tip_amount = (bill * Decimal(tip_percent)) / Decimal(100)
    total = bill + tip_amount
    per_person = (total / people).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return per_person
