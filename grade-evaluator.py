#!/usr/bin/python3
"""Grade Evaluator Application

Calculates student GPA, validates assignment grades and weight distributions,
and determines pass/fail status and resubmission eligibility based on CSV input.
"""

import csv
import os
import sys


def load_csv_data():
    """Prompts for a filename, verifies existence, and loads rows."""
    filename = input(
        "Enter the name of the CSV file to process (e.g., grades.csv): "
    )
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignment_val = row.get('assignment') or row.get('Assignment')
                group_val = (
                    row.get('group') or row.get('Category') or row.get('Group')
                )
                score_val = row.get('score') or row.get('Score')
                weight_val = row.get('weight') or row.get('Weight')

                if not all([assignment_val, group_val, score_val, weight_val]):
                    print("Error: Missing required columns in CSV row.")
                    sys.exit(1)

                assignments.append({
                    'assignment': assignment_val,
                    'group': group_val,
                    'score': float(score_val),
                    'weight': float(weight_val)
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """Processes assignment records and prints final academic standing."""
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: The CSV file is completely empty.")
        return

    total_weight = 0.0
    summative_weight = 0.0
    formative_weight = 0.0

    summative_weighted_score = 0.0
    formative_weighted_score = 0.0

    failed_formatives = []

    for item in data:
        assignment = item['assignment']
        group = item['group'].strip().capitalize()
        score = item['score']
        weight = item['weight']

        if not (0 <= score <= 100):
            print(f"Error: Score {score} for '{assignment}' out of range.")
            return

        total_weight += weight

        if group == 'Summative':
            summative_weight += weight
            summative_weighted_score += score * (weight / 100.0)
        elif group == 'Formative':
            formative_weight += weight
            formative_weighted_score += score * (weight / 100.0)
            if score < 50.0:
                failed_formatives.append(item)
        else:
            print(f"Error: Unknown group '{group}' for '{assignment}'.")
            return

    if round(total_weight, 2) != 100.0:
        print(f"Error: Total weight sum is {total_weight}%, expected 100%.")
        return

    if round(summative_weight, 2) != 40.0:
        print(f"Error: Summative weight is {summative_weight}%, expected 40%.")
        return

    if round(formative_weight, 2) != 60.0:
        print(f"Error: Formative weight is {formative_weight}%, expected 60%.")
        return

    summative_pct = (summative_weighted_score / 40.0) * 100.0
    formative_pct = (formative_weighted_score / 60.0) * 100.0

    total_grade = summative_weighted_score + formative_weighted_score
    gpa = (total_grade / 100.0) * 5.0

    passed = (summative_pct >= 50.0) and (formative_pct >= 50.0)
    status = "PASSED" if passed else "FAILED"

    print(f"Summative Score : {summative_pct:.2f}% (Weight: 40%)")
    print(f"Formative Score : {formative_pct:.2f}% (Weight: 60%)")
    print(f"Overall Grade   : {total_grade:.2f}%")
    print(f"Final GPA       : {gpa:.2f} / 5.0")
    print(f"Final Status    : {status}")
    print("-" * 30)

    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        eligible = [
            item['assignment'] for item in failed_formatives
            if item['weight'] == max_weight
        ]
        print("Resubmission Candidates (Highest Weight Failed Formative):")
        for name in eligible:
            print(f" - {name}")
    else:
        print("Resubmission Candidates: None")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
