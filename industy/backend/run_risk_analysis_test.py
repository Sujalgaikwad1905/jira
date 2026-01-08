"""
Test the risk analysis functionality
"""
import asyncio
from services.risk_service import run_risk_analysis
from db.mongodb import connect_to_mongo

async def test_risk_analysis():
    print('Connecting to database...')
    await connect_to_mongo()
    print('Running risk analysis...')
    results = await run_risk_analysis()
    print(f'Created {len(results)} new risk alerts')
    for risk in results:
        print(f'  - {risk["task_key"]}: {risk["assignee"]} - {risk["risk_level"]}')

if __name__ == "__main__":
    asyncio.run(test_risk_analysis())