# MultiDesk JIRA Dashboard

A comprehensive JIRA dashboard solution that integrates with JIRA Cloud to provide enhanced project management capabilities with automated risk detection for employee leave vs. task due date overlaps.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)

## Overview

MultiDesk bridges the gap between JIRA project management and team availability tracking by providing automated risk detection for potential delivery delays. The system synchronizes JIRA tasks with employee leave schedules to identify when critical deadlines may be impacted by team member unavailability.

### Key Benefits:
- **Risk Prevention**: Proactive identification of potential delivery risks
- **Team Visibility**: Complete visibility into team availability and workload
- **JIRA Integration**: Seamless integration with existing JIRA workflows
- **Automated Alerts**: Real-time risk detection and alerting
- **Scalable Architecture**: Designed to handle enterprise-level data volumes

## Features

### 1. JIRA Integration
- **Real-time Sync**: Automatic synchronization of JIRA projects, tasks, stories, epics, and bugs
- **Admin Access**: Supports admin-level access to view all tasks in projects (not just assigned tasks)
- **Multiple Issue Types**: Comprehensive handling of all JIRA issue types
- **Smart Filtering**: Optimized JQL queries for efficient data retrieval
- **Secure Connection**: Encrypted API token storage and secure authentication

### 2. Leave Management
- **CSV Upload**: Simple employee leave data upload via CSV format
- **Flexible Dates**: Support for various date formats and ranges
- **Email Matching**: Automatic correlation between JIRA assignees and employee emails
- **Bulk Processing**: Efficient batch processing of multiple leave entries
- **Data Validation**: Comprehensive validation for data integrity

### 3. Risk Detection
- **Automated Analysis**: Real-time risk detection after leave data upload
- **Date Overlap Detection**: Advanced algorithms to identify due date/leave overlaps
- **Risk Scoring**: Dynamic risk level assignment (HIGH/MEDIUM/LOW)
- **Impact Assessment**: Cross-team impact analysis and reporting
- **Alert System**: Visual risk indicators and notification system

### 4. Dashboard Visualization
- **Real-time Updates**: Live dashboard with current risk status
- **Visual Indicators**: Color-coded risk alerts and priority indicators
- **Data Tables**: Comprehensive task and risk data presentation
- **Filtering Options**: Advanced filtering and search capabilities
- **Responsive Design**: Mobile-friendly interface for anywhere access

### 5. Security & Authentication
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Different access levels for team members
- **Encrypted Storage**: Secure storage of sensitive credentials
- **Session Management**: Proper session handling and expiration

## Architecture

### Tech Stack
- **Frontend**: React 18 + Vite + TypeScript
- **Backend**: Python 3.13 + FastAPI + MongoDB
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT with secure token management
- **File Processing**: Pandas for CSV handling
- **Styling**: Tailwind CSS + shadcn/ui components

### System Components
```
industy/
├── backend/              # Python FastAPI server
│   ├── routers/          # API route handlers
│   ├── services/         # Business logic
│   ├── models/           # Data models
│   ├── db/               # Database connections
│   └── utils/            # Utility functions
├── frontend/             # React/Vite client
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Route components
│   │   ├── services/     # API clients
│   │   └── hooks/        # Custom React hooks
│   └── public/           # Static assets
└── uploads/              # File upload directory
```

### Data Flow Architecture
```
1. JIRA Integration: JIRA API → Backend Service → MongoDB Storage → Dashboard Display
2. Leave Upload: CSV File → File Upload → Leave Processing → Risk Analysis → Alerts
3. Risk Detection: Task Due Dates + Leave Periods → Overlap Detection → Risk Alerts
4. Dashboard: MongoDB Data → API Requests → Real-time Updates → UI Components
```

## Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.13+ (for backend)
- MongoDB Community Server
- JIRA Cloud account with API access

### Getting Started
```bash
# Clone the repository
git clone <repository-url>
cd industy

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Frontend Setup
cd ../frontend
npm install

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Start backend
cd backend
uvicorn main:app --reload

# Start frontend (in new terminal)
cd frontend
npm run dev
```

## Installation

### Backend Installation
1. **Python Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   - Install MongoDB Community Server
   - Start MongoDB service
   - Verify connection with `mongod`

3. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

### Frontend Installation
1. **Node.js Dependencies**:
   ```bash
   npm install
   ```

2. **Frontend Configuration**:
   - Update API endpoints in `src/services/api.js`
   - Configure proxy settings if needed

## Configuration

### Backend Configuration (.env)
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=multidesk

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USER=your-email@gmail.com
MAIL_PASS=your-app-password
MAIL_FROM=your-email@gmail.com

# OTP Configuration
OTP_EXPIRE_MINUTES=10
```

### JIRA Setup
1. **Create API Token**:
   - Go to JIRA: Profile → Account settings → Security → API tokens
   - Create and copy the API token

2. **Domain Configuration**:
   - Format: `https://yourcompany.atlassian.net`
   - Ensure correct company name

3. **Permissions**:
   - Ensure account has admin or project access rights
   - Verify API access permissions

## Usage Guide

### 1. Initial Setup
1. **Register/Login**: Create account or sign in to the dashboard
2. **Connect JIRA**: Enter JIRA credentials and connect your account
3. **Verify Connection**: Confirm successful JIRA integration
4. **Initial Sync**: Allow system to sync existing JIRA data

### 2. Managing Employee Leaves
1. **Prepare CSV File**: Format with columns: `employee_email`, `leave_start`, `leave_end`
2. **Upload File**: Navigate to "Data Management" → Upload CSV
3. **Monitor Processing**: Track file status and record count
4. **Review Results**: Check for successful processing in leave management

### 3. Risk Monitoring
1. **Access Dashboard**: Navigate to main dashboard
2. **View Risk Alerts**: See current risk status and details
3. **Filter Risks**: Use filters to focus on specific timeframes or priorities
4. **Take Action**: Address identified risks before they impact delivery

### 4. Task Management
1. **View Tasks**: Browse synchronized JIRA tasks
2. **Filter Options**: Use advanced filtering for specific views
3. **Risk Correlation**: Identify tasks with potential leave conflicts
4. **Export Data**: Export filtered data for reporting

## API Documentation

### Backend API Endpoints

#### Authentication
```
POST /api/auth/login          # User login
POST /api/auth/register       # User registration
GET /api/auth/me             # Get current user
POST /api/auth/logout        # Logout user
```

#### JIRA Integration
```
POST /api/jira/connect       # Connect JIRA account
POST /api/jira/sync          # Sync JIRA data
GET /api/jira/tasks          # Get all tasks
GET /api/jira/projects       # Get all projects
GET /api/jira/connection-status  # Check connection status
```

#### File Management
```
POST /api/files/upload       # Upload leave CSV
GET /api/files/             # Get uploaded files
GET /api/files/{id}         # Get specific file
DELETE /api/files/{id}      # Delete file
```

#### Risk Detection
```
GET /api/risks              # Get all risk alerts
GET /api/risks/{id}         # Get specific risk
POST /api/risks/analyze     # Trigger risk analysis
DELETE /api/risks/clear     # Clear all risks
```

### Frontend Components

#### Dashboard Components
- **StatCard**: Summary statistics and metrics
- **AnalyticsCharts**: Visual data representations
- **RiskIndicator**: Persistent risk alert button
- **TaskTable**: Comprehensive task listing
- **RiskTable**: Risk alert management

#### Navigation Components
- **ProtectedRoute**: Authentication wrapper
- **Sidebar**: Main navigation menu
- **Header**: Top navigation and user controls

#### Data Management Components
- **FileUpload**: Drag-and-drop file upload
- **LeaveCalendar**: Calendar view of leave schedules
- **RiskTimeline**: Timeline view of risk periods

## Development

### Backend Development
```bash
# Start development server with auto-reload
uvicorn main:app --reload

# Run tests
python -m pytest tests/

# Format code
black .
```

### Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

### Adding New Features
1. **Backend**: Add new endpoints in `routers/` and business logic in `services/`
2. **Models**: Define new data models in `models/`
3. **Frontend**: Create new components in `components/` and pages in `pages/`
4. **Services**: Add API calls in `services/`
5. **Testing**: Add comprehensive tests for all new functionality

## Troubleshooting

### Common Issues

#### JIRA Connection Problems
- **Symptom**: "Invalid JIRA connection" error
- **Solution**: Verify API token, email, and domain match exactly
- **Check**: Ensure JIRA account has necessary permissions

#### File Upload Issues
- **Symptom**: Upload succeeds but no records processed
- **Solution**: Verify CSV format has correct headers
- **Check**: Ensure date format is YYYY-MM-DD

#### Risk Detection Not Working
- **Symptom**: No risks detected despite overlapping dates
- **Solution**: Verify email addresses match between systems
- **Check**: Confirm date ranges actually overlap

#### Database Connection Issues
- **Symptom**: Cannot connect to MongoDB
- **Solution**: Verify MONGODB_URL configuration
- **Check**: Ensure MongoDB service is running

### Debugging Commands
```bash
# Check MongoDB connection
mongo --host localhost:27017

# Backend logs
tail -f backend/logs/app.log

# Frontend console
npm run dev  # Check browser console
```

### Support Resources
- Check logs for detailed error information
- Verify all configuration values
- Ensure all services are running
- Contact development team for complex issues

## Deployment

### Production Requirements
- **Server**: Node.js 18+, Python 3.13+
- **Database**: MongoDB Atlas or self-hosted MongoDB
- **SSL Certificate**: Required for production
- **Environment Variables**: Properly configured for production

### Deployment Steps
1. **Build Frontend**: `npm run build`
2. **Configure Backend**: Set production environment variables
3. **Deploy Backend**: Deploy Python application with WSGI server
4. **Serve Frontend**: Serve built frontend files
5. **Setup Reverse Proxy**: Configure nginx/Apache for SSL termination

### Environment Configuration
```env
# Production
DEBUG=False
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
SECRET_KEY=production-secure-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
```

### Monitoring & Maintenance
- **Database**: Monitor connection pools and performance
- **API**: Track response times and error rates
- **Files**: Monitor upload success rates
- **Risks**: Track detection accuracy and alerts

---

## Support & Contact

For technical support, feature requests, or issues:
- **Documentation**: Check the API documentation and guides
- **Logs**: Review application logs for detailed error information
- **Community**: Join the developer community for assistance
- **Issues**: Submit GitHub issues for bugs or feature requests

**Project Version**: 1.0.0
**Last Updated**: January 2026
**License**: [Specify License]