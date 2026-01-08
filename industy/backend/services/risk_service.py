from datetime import datetime, date
from db import get_database
import logging

logger = logging.getLogger(__name__)

async def run_risk_analysis():
    """Analyze tasks for leave-related risks"""
    db = get_database()

    tasks = db.jira_tasks
    leaves = db.leaves
    risks = db.risk_alerts

    created = []
    
    # Clear all existing risks before running new analysis
    logger.info("🗑️ Clearing existing risk alerts...")
    delete_result = await risks.delete_many({})
    logger.info(f"🗑️ Deleted {delete_result.deleted_count} existing risk alerts")
    
    task_count = 0
    checked_count = 0
    skipped_count = 0

    logger.info("🔍 Starting risk analysis...")
    
    async for task in tasks.find():
        task_count += 1
        assignee_email = task.get("assignee_email")
        due_date = task.get("duedate")
        task_key = task.get("key", "UNKNOWN")

        logger.debug(f"Task {task_key}: assignee_email={assignee_email}, duedate={due_date}")

        # Skip if no assignee email or due date
        if not assignee_email:
            logger.debug(f"❌ Skipping {task_key}: No assignee_email")
            skipped_count += 1
            continue
            
        if not due_date:
            logger.debug(f"❌ Skipping {task_key}: No due_date")
            skipped_count += 1
            continue

        # Convert due_date to date if it's a datetime
        if isinstance(due_date, datetime):
            due_date_obj = due_date.date()
            due_date_query = due_date  # Use datetime for query
        elif isinstance(due_date, date):
            due_date_obj = due_date
            # Convert date to datetime for MongoDB query
            due_date_query = datetime.combine(due_date, datetime.min.time())
        else:
            logger.debug(f"❌ Skipping {task_key}: Invalid date type {type(due_date)}")
            skipped_count += 1
            continue
        
        checked_count += 1
        
        # Normalize email to lowercase for comparison
        assignee_email_lower = assignee_email.lower().strip()
        
        logger.debug(f"🔎 Checking {task_key} - Assignee: {assignee_email_lower}, Due: {due_date_obj}")

        # Find overlapping leave - IMPROVED QUERY
        # Check if the due date falls within the leave period
        # Ensure consistent datetime comparison
        
        # The due_date_query is already a datetime object
        # Ensure we compare dates properly
        leave = await leaves.find_one({
            "employee_email": assignee_email_lower,
            "leave_start": {"$lte": due_date_query},
            "leave_end": {"$gte": due_date_query}
        })
        
        if not leave:
            # Try alternate query for debugging
            all_leaves_for_user = await leaves.count_documents({
                "employee_email": assignee_email_lower
            })
            logger.debug(f"   No overlap found. User has {all_leaves_for_user} leave records total")
            continue

        logger.info(f"⚠️ OVERLAP FOUND for {task_key}!")
        logger.info(f"   Task due: {due_date_obj}")
        logger.info(f"   Leave: {leave['leave_start']} to {leave['leave_end']}")
        
        # Create new risk alert
        risk = {
            "task_key": task_key,
            "task_title": task.get("summary", "No title"),
            "assignee": assignee_email_lower,
            "due_date": datetime.combine(due_date_obj, datetime.min.time()) if isinstance(due_date_obj, date) and not isinstance(due_date_obj, datetime) else due_date_obj,  # Convert date to datetime for MongoDB
            "leave_start": leave["leave_start"],
            "leave_end": leave["leave_end"],
            "risk_level": "HIGH",
            "status": "OPEN",
            "created_at": datetime.utcnow()
        }

        await risks.insert_one(risk)
        created.append(risk)
        logger.info(f"✅ Created risk alert for {task_key} - {assignee_email_lower} on leave")
    
    logger.info(f"📊 Analysis complete: {task_count} total tasks, {checked_count} checked, {skipped_count} skipped")
    logger.info(f"🚨 {len(created)} new risk alerts created")

    return created
