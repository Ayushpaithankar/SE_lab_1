import math


def parse_claim(text):
    """Return a normalized warranty plan and its non-negative age.

    Malformed claims use a predictable default instead of raising an exception.
    """
    if not isinstance(text, str):
        return "Unknown", 0.0

    try:
        plan, months_text = text.split(":", 1)
        months = float(months_text.strip())
    except (TypeError, ValueError):
        return "Unknown", 0.0

    plan = plan.strip()
    if not plan or not math.isfinite(months) or months < 0:
        return "Unknown", 0.0

    return plan.title(), months


def age_average(ages_csv):
    """Return the floor average of non-negative product ages, or zero."""
    if not isinstance(ages_csv, str) or not ages_csv.strip():
        return 0

    try:
        values = [int(age.strip()) for age in ages_csv.split(",")]
    except (TypeError, ValueError):
        return 0

    if not values or any(age < 0 for age in values):
        return 0

    return sum(values) // len(values)


def payable_charge(text):
    """Return the payable charge after tax and discount, or zero."""
    if not isinstance(text, str):
        return 0.0

    try:
        charge_text, discount_text = text.split("|", 1)
        charge = float(charge_text.strip())
        discount = float(discount_text.strip())
    except (TypeError, ValueError):
        return 0.0

    if (
        not math.isfinite(charge)
        or not math.isfinite(discount)
        or charge < 0
        or discount < 0
    ):
        return 0.0

    return max(charge * 1.18 - discount, 0.0)


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
