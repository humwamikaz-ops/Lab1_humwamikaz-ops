#!/bin/bash

ARCHIVE_DIR="./archive"
LOG_FILE="./organizer.log"

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Created directory: $ARCHIVE_DIR" >> "$LOG_FILE"
fi

found_files=0
for file in *.csv; do
    if [ -f "$file" ]; then
        found_files=1
        TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
        FILENAME=$(basename "$file" .csv)
        NEW_FILENAME="${FILENAME}_${TIMESTAMP}.csv"

        mv "$file" "$ARCHIVE_DIR/$NEW_FILENAME"

        echo "$(date '+%Y-%m-%d %H:%M:%S') - Archived: $file -> $ARCHIVE_DIR/$NEW_FILENAME" >> "$LOG_FILE"
        echo "Successfully archived '$file' as '$NEW_FILENAME'."
    fi
done

if [ $found_files -eq 0 ]; then
    echo "No CSV files found to archive."
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Run complete: No CSV files found." >> "$LOG_FILE"
fi
