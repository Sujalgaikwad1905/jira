"""
Test risk analysis directly
"""
import asyncio
from db import connect_to_mongo, close_mongo_connection
from services.risk_service import run_risk_analysis

async def test_risk():
    await connect_to_mongo()
    
    print("\n" + "="*70)
    print("TESTING RISK ANALYSIS")
    print("="*70)
    
    risks = await run_risk_analysis()
    
    print(f"\n✅ Analysis complete!")
    print(f"🚨 Created {len(risks)} risk alerts")
    
    if risks:
        print("\nRisk alerts created:")
        for risk in risks:
            print(f"  - {risk['task_key']}: {risk['assignee']} on leave {risk['leave_start']} to {risk['leave_end']}")
    
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(test_risk())
