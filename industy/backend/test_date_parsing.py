"""
Test script to verify date parsing for MongoDB compatibility
"""
import asyncio
from datetime import datetime
from services.jira_service import parse_jira_date, parse_jira_datetime

def test_date_parsing():
    print("🔍 Testing date parsing functions...")
    
    # Test parse_jira_date function
    print("\n📅 Testing parse_jira_date:")
    test_dates = [
        "2025-01-15",  # Valid date
        "2025-12-31",  # Another valid date
        "invalid-date",  # Invalid date
        None,  # None value
        ""  # Empty string
    ]
    
    for date_str in test_dates:
        try:
            result = parse_jira_date(date_str)
            print(f"  Input: {date_str} -> Output: {result} (Type: {type(result).__name__})")
        except Exception as e:
            print(f"  Input: {date_str} -> Error: {e}")
    
    # Test parse_jira_datetime function
    print("\n🕒 Testing parse_jira_datetime:")
    test_datetimes = [
        "2025-01-15T10:30:00.000+0000",
        "2025-12-31T23:59:59Z",
        "invalid-datetime",
        None,
        ""
    ]
    
    for dt_str in test_datetimes:
        try:
            result = parse_jira_datetime(dt_str)
            print(f"  Input: {dt_str} -> Output: {result} (Type: {type(result).__name__})")
        except Exception as e:
            print(f"  Input: {dt_str} -> Error: {e}")
    
    print("\n✅ Date parsing test completed!")

if __name__ == "__main__":
    test_date_parsing()