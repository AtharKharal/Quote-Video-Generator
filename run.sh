#!/bin/bash

# Check if iteration count is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <number_of_iterations>"
  exit 1
fi

ITERATIONS=$1

for ((i=1; i<=ITERATIONS; i++))
do
  echo "Iteration $i/$ITERATIONS..."

  python src/vid_generator.py && python src/publisher.py output.mp4

  # Optional: check if the previous command failed
  if [ $? -ne 0 ]; then
    echo "Error occurred in iteration $i. Stopping..."
    exit 1
  fi
done

echo "All iterations completed."