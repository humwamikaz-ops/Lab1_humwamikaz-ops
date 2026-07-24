#!/bin/bash

ARCHIVE_DIR="archive"
ORIGINAL_FILE="grades.csv"
LOG_FILE="organizer.log"

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
fi

if [ -f "$ORIGINAL_FILE" ]; then
    TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
    ARCHIVED_FILENAME="grades_${TIMESTAMP}.csv"
    ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_FILENAME}"

    mv "$ORIGINAL_FILE" "$ARCHIVED_PATH"
    echo "assignment,group,score,weight" > "$ORIGINAL_FILE"

    LOG_ENTRY="[${TIMESTAMP}] Archived: ${ORIGINAL_FILE} -> ${ARCHIVED_PATH}"
    echo "$LOG_ENTRY" >> "$LOG_FILE"
    echo "Successfully archived ${ORIGINAL_FILE} to ${ARCHIVED_PATH}"
else
    echo "Error: ${ORIGINAL_FILE} does not exist in current directory."
    exit 1
fi
