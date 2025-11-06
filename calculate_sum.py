#!/usr/bin/env python3
"""
Download script.js from the js_table folder and sum all numbers found in it.
"""

import re
import requests
from urllib.parse import urljoin

BASE_PAGE = "https://sanand0.github.io/tdsdata/js_table/?seed=23"
# Direct script URL (as shown in DevTools)
SCRIPT_URL = "https://sanand0.github.io/tdsdata/js_table/script.js"

def fetch_text(url, timeout=15):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text

def extract_numbers(text):
    """
    Match:
      - optional sign
      - integer with optional thousands separators (e.g., 1,234 or 1234)
      - optional decimal part
    Returns list of floats.
    """
    pattern = r'[-+]?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?'
    matches = re.findall(pattern, text)
    nums = []
    for m in matches:
        # skip isolated + or - (regex shouldn't match them alone but be safe)
        if m in ("+", "-"):
            continue
        # remove commas used as thousands separator
        cleaned = m.replace(",", "")
        try:
            nums.append(float(cleaned))
        except ValueError:
            # ignore any weird tokens that can't parse
            continue
    return nums

def main():
    try:
        js_text = fetch_text(SCRIPT_URL)
    except requests.RequestException as e:
        print("Failed to fetch script.js:", e)
        return

    print("=== script.js (first 1200 characters) ===\n")
    print(js_text[:1200])
    print("\n=== end snippet ===\n")

    numbers = extract_numbers(js_text)
    if not numbers:
        print("No numbers found in script.js.")
        return

    total = sum(numbers)

    # Display results neatly: integers as ints if appropriate
    if all(n.is_integer() for n in numbers):
        total_display = int(total)
    else:
        total_display = total

    print(f"Found {len(numbers)} numeric tokens in script.js.")
    print("Sum of numbers:", total_display)

if __name__ == "__main__":
    main()
