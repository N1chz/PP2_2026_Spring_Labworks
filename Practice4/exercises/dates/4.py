from datetime import datetime

date1 = datetime(2025, 2, 20, 12, 0, 0)
date2 = datetime(2025, 2, 25, 12, 0, 0)

difference = date2 - date1
difference_in_seconds = difference.total_seconds()

print(f"Difference in seconds: {difference_in_seconds}")
