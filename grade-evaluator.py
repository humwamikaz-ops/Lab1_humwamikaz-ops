cat << 'EOF' > grade-evaluator.py
#!/usr/bin/python3
"""Student performance and Grade assesor

Application calculates GPA, flags resubmission students and also evaluates
pass and fail status
"""

import csv
import os
import sys


def parse_grade_records():
    """Prompts for target CSV file and extracts assessment records."""
    filetarget = input("Enter path to grades CSV (e.g., grades.csv): ")

    if not os.path.exists(filetarget):
        print(f"Error: Unable to locate file '{filetarget}'.")
        sys.exit(1)

    grade_records = []
    try:
        with open(filetarget, mode='r', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            for row in reader:
                task_title = row.get('assignment') or row.get('Assignment')
                category = (
                    row.get('group') or row.get('Category') or row.get('Group')
                )
                mark = row.get('score') or row.get('Score')
                weight_val = row.get('weight') or row.get('Weight')

                if not all([task_title, category, mark, weight_val]):
                    print("Error: Incomplete column headers in CSV input.")
                    sys.exit(1)

                grade_records.append({
                    'assignment': task_title,
                    'group': category,
                    'score': float(mark),
                    'weight': float(weight_val)
                })
        return grade_records
    except Exception as err:
        print(f"An error occurred while parsing the dataset: {err}")
        sys.exit(1)


def analyze_academic_standing(dataset):
    """Calculates overall metrics, weight integrity, and pass/fail standing."""
    print("\n" + "=" * 36)
    print("      ACADEMIC EVALUATION REPORT    ")
    print("=" * 36)

    if not dataset:
        print("Error: Input file contains no records to process.")
        return

    cum_weight = 0.0
    sum_weight_total = 0.0
    form_weight_total = 0.0

    sum_weighted_points = 0.0
    form_weighted_points = 0.0

    unpassed_formatives = []

    for entry in dataset:
        task = entry['assignment']
        category_name = entry['group'].strip().capitalize()
        score_val = entry['score']
        weight_val = entry['weight']

        # a) Check if all scores are percentage based (0-100)
        if not (0 <= score_val <= 100):
            print(f"Error: Score {score_val} for '{task}' out of range.")
            return

        cum_weight += weight_val

        if category_name == 'Summative':
            sum_weight_total += weight_val
            sum_weighted_points += score_val * (weight_val / 100.0)
        elif category_name == 'Formative':
            form_weight_total += weight_val
            form_weighted_points += score_val * (weight_val / 100.0)
            # e) Check for failed formative assignments (< 50%)
            if score_val < 50.0:
                unpassed_formatives.append(entry)
        else:
            print(f"Error: Unrecognized group '{category_name}' in '{task}'.")
            return

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    if round(cum_weight, 2) != 100.0:
        print(f"Error: Cumulative weight is {cum_weight}%, expected 100%.")
        return

    if round(sum_weight_total, 2) != 40.0:
        sum_err = f"Summative weight sum is {sum_weight_total}%, expected 40%."
        print(f"Error: {sum_err}")
        return

    if round(form_weight_total, 2) != 60.0:
        form_err = f"Formative weight sum is {form_weight_total}%, expected 60%."
        print(f"Error: {form_err}")
        return

    # Compute category averages
    sum_average = (sum_weighted_points / 40.0) * 100.0
    form_average = (form_weighted_points / 60.0) * 100.0

    # c) Calculate Final Grade & GPA
    final_score = sum_weighted_points + form_weighted_points
    calculated_gpa = (final_score / 100.0) * 5.0

    # d) Determine Pass/Fail status
    has_passed = (sum_average >= 50.0) and (form_average >= 50.0)
    standing = "PASSED" if has_passed else "FAILED"

    # f) Print final summary report
    print(f"Summative Average : {sum_average:.2f}% (Weighted 40%)")
    print(f"Formative Average : {form_average:.2f}% (Weighted 60%)")
    print(f"Overall Mark      : {final_score:.2f}%")
    print(f"Calculated GPA    : {calculated_gpa:.2f} / 5.0")
    print(f"Final Standing    : {standing}")
    print("-" * 36)

    # Output resubmission eligibility
    if unpassed_formatives:
        highest_failed_weight = max(
            item['weight'] for item in unpassed_formatives
        )
        resub_options = [
            item['assignment'] for item in unpassed_formatives
            if item['weight'] == highest_failed_weight
        ]
        print("Eligible Formative Resubmissions (Top-Weighted Unpassed):")
        for title in resub_options:
            print(f" - {title}")
    else:
        print("Eligible Formative Resubmissions: None")


if __name__ == "__main__":
    loaded_data = parse_grade_records()
    analyze_academic_standing(loaded_data)
EOF
