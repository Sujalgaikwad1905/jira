# PowerShell script to upload demo file and check risks

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "UPLOADING DEMO FILE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Upload the file
$filePath = "d:\working\industy\uploads\demo_sujal.csv"
$url = "http://localhost:8000/api/files/upload"

Write-Host "Uploading: $filePath" -ForegroundColor Yellow

$form = @{
    file = Get-Item -Path $filePath
}

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Form $form
    Write-Host "`n✅ Upload successful!" -ForegroundColor Green
    Write-Host "File ID: $($response.id)" -ForegroundColor White
    Write-Host "Status: $($response.status)" -ForegroundColor White
} catch {
    Write-Host "`n❌ Upload failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n⏳ Waiting 3 seconds for background processing..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CHECKING RISK ALERTS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check risks
$risksUrl = "http://localhost:8000/api/risks"

try {
    $risks = Invoke-RestMethod -Uri $risksUrl -Method Get
    
    if ($risks.Count -eq 0) {
        Write-Host "No risks found yet. Try triggering manually:" -ForegroundColor Yellow
        Write-Host "  curl http://localhost:8000/api/risks/check" -ForegroundColor White
    } else {
        Write-Host "✅ Found $($risks.Count) risk alert(s)!`n" -ForegroundColor Green
        
        foreach ($risk in $risks) {
            if ($risk.assignee -eq "sujalgaikwadusa@gmail.com") {
                Write-Host "🚨 RISK DETECTED FOR DEMO USER!" -ForegroundColor Red
                Write-Host "  Task: $($risk.task_key)" -ForegroundColor White
                Write-Host "  Title: $($risk.task_title)" -ForegroundColor White
                Write-Host "  Assignee: $($risk.assignee)" -ForegroundColor White
                Write-Host "  Due Date: $($risk.due_date)" -ForegroundColor White
                Write-Host "  Leave: $($risk.leave_start) to $($risk.leave_end)" -ForegroundColor White
                Write-Host "  Risk Level: $($risk.risk_level)" -ForegroundColor Red
                Write-Host "  Status: $($risk.status)" -ForegroundColor Yellow
                Write-Host ""
            }
        }
    }
} catch {
    Write-Host "❌ Failed to get risks: $_" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DEMO COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
