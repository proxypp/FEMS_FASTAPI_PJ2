# 업데이트 배포 스크립트 (관리자 권한으로 실행)
$projectPath = "D:\srv\fems_fastApi"
$nssm = "D:\nssm-2.24\win64\nssm.exe"

Write-Host "배포 시작..."

Set-Location $projectPath

git pull
if ($LASTEXITCODE -ne 0) { Write-Host "git pull 실패"; exit 1 }

uv sync --no-dev
if ($LASTEXITCODE -ne 0) { Write-Host "패키지 설치 실패"; exit 1 }

& $nssm restart fems_fastapi

Write-Host "배포 완료!"
