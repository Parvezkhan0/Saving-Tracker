

# Savings Goals Tracker

The Savings Goals Tracker is a simple Python script that helps you keep track of your progress towards your savings goals. It takes input from a JSON file containing your savings goals and displays information such as the goal name, start date, end date, percentage completed, and more.

## Features

- Tracks multiple savings goals with customizable parameters.
- Calculates the amount saved on a fortnightly basis.
- Provides a summary of total savings needed and fortnightly savings target.

## Usage

1. **Installation:** 

    - Make sure you have Python installed on your system.

2. **Setup:**

    - Clone or download the repository to your local machine.

3. **Usage:**

    - Run the script using the following command:
        ```
        python savings_goals_tracker.py --file <path_to_savings_file.json>
        ```
        - Replace `<path_to_savings_file.json>` with the path to your JSON file containing savings goals.

4. **JSON File Format:**

    - The JSON file should have the following structure:
        ```json
        {
            "base": 1000,
            "goals": [
                {
                    "name": "Goal 1",
                    "amount": 5000,
                    "start_date": "2023-11-01T00:00:00Z",
                    "spend_date": "2023-12-01T00:00:00Z"
                },
                {
                    "name": "Goal 2",
                    "amount": 3000,
                    "start_date": "2023-11-15T00:00:00Z",
                    "spend_date": "2023-12-15T00:00:00Z"
                }
            ]
        }
        ```
        - `base`: Base savings amount (optional).
        - `goals`: List of savings goals, each with a name, amount, start date, and end date.

5. **Output:**

    - The script will display a table summarizing your savings goals, including the goal name, start date, end date, percentage completed, fortnightly savings target, and amount saved.

6. **Fortnightly Amount:**

    - Displays the total fortnightly savings target.

7. **Total:**

    - Displays the total amount needed to achieve all savings goals.

## Example

- An example JSON file (`savings_data.json`) and usage is provided in the repository.

