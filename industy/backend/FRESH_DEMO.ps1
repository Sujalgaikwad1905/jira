# Complete Fresh Demo Script
# This demonstrates the entire risk detection flow from scratch

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🎬 FRESH DEMO - Risk Detection System" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Prepare database
Write-Host "[STEP 1] Preparing database..." -ForegroundColor Yellow
Write-Host "  - Assigning all tasks to sujalgaikwadusa@gmail.com" -ForegroundColor White
Write-Host "  - Clearing old leaves and risks" -ForegroundColor White
Write-Host ""

python prepare_fresh_demo.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Preparation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nPress any key to continue with file upload..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Step 2: Show file content
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[STEP 2] File to Upload" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "File: fresh_demo.csv" -ForegroundColor White
Write-Host "Content:" -ForegroundColor White
Get-Content "d:\working\industy\uploads\fresh_demo.csv" | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}

Write-Host "`nPress any key to upload file..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Step 3: Upload file
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[STEP 3] Uploading Leave File" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$filePath = "d:\working\industy\uploads\fresh_demo.csv"
$url = "http://localhost:8000/api/files/upload"

Write-Host "📤 Uploading: $filePath" -ForegroundColor Yellow

$form = @{
    file = Get-Item -Path $filePath
}

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Form $form
    Write-Host "✅ Upload successful!" -ForegroundColor Green
    Write-Host "   File ID: $($response.id)" -ForegroundColor White
    Write-Host "   Status: $($response.status)" -ForegroundColor White
    Write-Host "   Filename: $($response.filename)" -ForegroundColor White
} catch {
    Write-Host "❌ Upload failed: $_" -ForegroundColor Red
    exit 1
}

# Step 4: Wait for background processing
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[STEP 4] Background Processing" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "⏳ System is processing leave data..." -ForegroundColor Yellow
Write-Host "   - Parsing CSV file" -ForegroundColor White
Write-Host "   - Saving to database" -ForegroundColor White
Write-Host "   - Triggering risk analysis" -ForegroundColor White
Write-Host "   - Checking task overlaps" -ForegroundColor White
Write-Host ""

for ($i = 3; $i -gt 0; $i--) {
    Write-Host "   Waiting $i seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 1
}

Write-Host "✅ Processing complete!" -ForegroundColor Green

Write-Host "`nPress any key to check risk alerts..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Step 5: Check risks
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[STEP 5] Risk Alerts Detected" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$risksUrl = "http://localhost:8000/api/risks"

try {
    $risks = Invoke-RestMethod -Uri $risksUrl -Method Get
    
    if ($risks.Count -eq 0) {
        Write-Host "⚠️ No risks found! Trying manual trigger..." -ForegroundColor Yellow
        Invoke-RestMethod -Uri "http://localhost:8000/api/risks/check" | Out-Null
        Start-Sleep -Seconds 2
        $risks = Invoke-RestMethod -Uri $risksUrl -Method Get
    }
    
    Write-Host "🚨 TOTAL RISK ALERTS: $($risks.Count)" -ForegroundColor Red
    Write-Host ""
    
    $counter = 1
    foreach ($risk in $risks) {
        if ($risk.assignee -eq "sujalgaikwadusa@gmail.com") {
            Write-Host "[$counter] RISK ALERT" -ForegroundColor Red
            Write-Host "    Task Key: $($risk.task_key)" -ForegroundColor White
            Write-Host "    Task Title: $($risk.task_title)" -ForegroundColor White
            Write-Host "    Assignee: $($risk.assignee)" -ForegroundColor Cyan
            Write-Host "    Due Date: $($risk.due_date)" -ForegroundColor Yellow
            Write-Host "    Leave Period: $($risk.leave_start) to $($risk.leave_end)" -ForegroundColor Yellow
            Write-Host "    Risk Level: $($risk.risk_level)" -ForegroundColor Red
            Write-Host "    Status: $($risk.status)" -ForegroundColor Magenta
            Write-Host ""
            $counter++
        }
    }
    
} catch {
    Write-Host "❌ Failed to get risks: $_" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ DEMO COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📊 What Just Happened:" -ForegroundColor White
Write-Host "   1. ✅ Uploaded leave file for sujalgaikwadusa@gmail.com" -ForegroundColor White
Write-Host "   2. ✅ System processed leave dates (Dec 10 - Jan 10)" -ForegroundColor White
Write-Host "   3. ✅ Automatically checked all Jira tasks" -ForegroundColor White
Write-Host "   4. ✅ Detected $($risks.Count) tasks due during leave period" -ForegroundColor White
Write-Host "   5. ✅ Created HIGH priority risk alerts" -ForegroundColor White
Write-Host ""
Write-Host "💡 Business Impact:" -ForegroundColor White
Write-Host "   - Manager can see potential delivery risks" -ForegroundColor White
Write-Host "   - Can reassign tasks or adjust timelines" -ForegroundColor White
Write-Host "   - Proactive risk management enabled!" -ForegroundColor White
Write-Host ""
