import argparse
from datetime import date
import json
import logging
import pathlib
import sys
from typing import List, NamedTuple

import iso8601

logger = logging.getLogger(__name__)


class SavingsGoal(NamedTuple):
    name: str
    amount: int
    start_date: date
    spend_date: date
    percentage: float
    fortnightly_amount: float
    target_savings: int


def main(savings_file: pathlib.Path) -> None:
    today = date.today()

    with savings_file.open("rb") as f_in:
        savings_data = json.load(f_in)

    name_len = 0
    amount_len = len("{}".format(savings_data.get("base", 0)))
    needed_savings = savings_data.get("base", 0)
    goals: List[SavingsGoal] = []
    fortnightly_total = 0.0

    for i, goal in enumerate(savings_data.get("goals", [])):
        start_date = iso8601.parse_date(goal["start_date"]).date()
        spend_date = iso8601.parse_date(goal["spend_date"]).date()
        total_days = (spend_date - start_date).days
        days_saved = (today - start_date).days
        percent_savings = min(1.0, days_saved / total_days)
        goal_name = goal.get("name", str(i))

        name_len = max(len(goal_name), name_len)
        amount_len = max(len("{:d}".format(goal["amount"])), amount_len)

        if start_date > spend_date:
            logger.warning(
                "start date of %s is greater than spend date of %s for item %s",
                start_date,
                spend_date,
                goal.get("name", i),
            )
            continue

        goals.append(
            SavingsGoal(
                goal_name,
                goal["amount"],
                start_date,
                spend_date,
                min(1.0, days_saved / total_days),
                14 * (goal["amount"] / total_days),
                int(percent_savings * goal["amount"]),
            )
        )

        needed_savings += int(percent_savings * goal["amount"])

    # Print the top part of the header
    print(
        "┏━{}━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━{}━┳━{}━┳━{}━┓".format(
            max(name_len, len("Name")) * "━",
            max(amount_len + 1, len("Goal")) * "━",
            max(amount_len + 1, len("Fortnightly Amount")) * "━",
            max(amount_len + 1, len("Amount Saved")) * "━",
        )
    )
    # Print the header labels
    print(
        "┃ {} ┃ Start Date ┃  End Date  ┃ Percentage ┃ {} ┃ {} ┃ {} ┃".format(
            "Name".center(max(name_len, len("Name"))),
            "Goal".center(max(amount_len + 1, len("Goal"))),
            "Fortnightly Amount".center(max(amount_len + 1, len("Fortnightly Amount"))),
            "Amount Saved".center(max(amount_len + 1, len("Amount Saved"))),
        )
    )
    # Print the bottom part of the header
    print(
        "┡━{}━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━{}━╇━{}━╇━{}━┩".format(
            max(name_len, len("Name")) * "━",
            max(amount_len + 1, len("Goal")) * "━",
            max(amount_len + 1, len("Fortnightly Amount")) * "━",
            max(amount_len + 1, len("Amount Saved")) * "━",
        )
    )

    # Print the individual goals
    for goal in goals:
        if goal.percentage < 1.0:
            fortnightly_amount = goal.fortnightly_amount
        else:
            fortnightly_amount = 0

        fortnightly_total += fortnightly_amount
        print(
            "│ {} │ {} │ {} │ {:10} │ ${} │ ${} │ ${} │".format(
                goal.name.ljust(max(name_len, len("Name"))),
                goal.start_date,
                goal.spend_date,
                "{:.0f}%".format(goal.percentage * 100),
                str(goal.amount).ljust(max(amount_len, len("Goal") - 1)),
                "{:.0f}".format(fortnightly_amount).ljust(
                    max(amount_len, len("Fortnightly Amount") - 1)
                ),
                str(goal.target_savings).ljust(
                    max(amount_len, len("Amount Saved") - 1)
                ),
            )
        )

    # Make a pseudo row for the base savings
    if savings_data.get("base", 0):
        print(
            "│ {} │            │            │            │ {} │ {} │ ${} │".format(
                "Base".ljust(max(name_len, len("Name"))),
                " " * max(amount_len + 1, len("Goal")),
                " " * max(amount_len + 1, len("Fortnightly Amount")),
                str(savings_data["base"]).ljust(
                    max(amount_len, len("Amount Saved") - 1)
                ),
            )
        )

    print(
        "└─{}─┴────────────┴────────────┴────────────┴─{}─┴─{}─┴─{}─┘".format(
            max(name_len, len("Name")) * "─",
            max(amount_len + 1, len("Goal")) * "─",
            max(amount_len + 1, len("Fortnightly Amount")) * "─",
            max(amount_len + 1, len("Amount Saved")) * "─",
        )
    )

    print("\nFortnightly Amount: ${:.0f}".format(fortnightly_total))
    print("Total: ${:.0f}".format(needed_savings))


def cli() -> int:
    parser = argparse.ArgumentParser(
        description="Simple script to help track progress towards savings goals"
    )
    parser.add_argument(
        "--file",
        required=True,
        type=pathlib.Path,
        help="Path to JSON file containing savings goals",
    )
    args = parser.parse_args()

    main(args.file)
    return 0


if __name__ == "__main__":
    sys.exit(cli())
