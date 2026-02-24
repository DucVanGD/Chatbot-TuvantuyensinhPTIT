# Script để làm sạch Git repository
# Xóa toàn bộ history và tạo commit mới

Write-Host "=== Cleaning Git Repository ===" -ForegroundColor Cyan
Write-Host ""

# Backup branch hiện tại
Write-Host "1. Creating backup branch..." -ForegroundColor Yellow
git branch backup-before-cleanup

# Tạo orphan branch mới (không có history)
Write-Host "2. Creating new orphan branch..." -ForegroundColor Yellow
git checkout --orphan new-main

# Add tất cả files hiện tại
Write-Host "3. Adding all current files..." -ForegroundColor Yellow
git add -A

# Commit
Write-Host "4. Creating clean commit..." -ForegroundColor Yellow
git commit -m "Initial commit - PTIT Admission Chatbot

Vietnamese chatbot for PTIT admission counseling
- Admission score lookup (2020-2025)
- Support for 34 majors
- 2 campuses: Hanoi and HCMC
- Custom Vietnamese tokenizer
- Built with RASA framework"

# Xóa branch main cũ
Write-Host "5. Deleting old main branch..." -ForegroundColor Yellow
git branch -D main

# Rename new-main thành main
Write-Host "6. Renaming new-main to main..." -ForegroundColor Yellow
git branch -m main

Write-Host ""
Write-Host "=== Clean up completed! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Repository now has only 1 commit with clean history." -ForegroundColor Green
Write-Host ""
Write-Host "To push to GitHub:" -ForegroundColor Yellow
Write-Host "  git push origin main --force" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: This will overwrite remote history!" -ForegroundColor Red
Write-Host ""
Write-Host "If something goes wrong, restore backup:" -ForegroundColor Yellow
Write-Host "  git checkout backup-before-cleanup" -ForegroundColor Cyan
