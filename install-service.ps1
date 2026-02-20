# 관리자 권한으로 실행 필요
$projectPath = "D:\srv\fems_fastApi"
$nssm = "D:\nssm-2.24\win64\nssm.exe"
$python = "$projectPath\.venv\Scripts\python.exe"

Write-Host "서비스 등록 중..."

& $nssm install fems_fastapi $python "-m" "fems_fastApi"
& $nssm set fems_fastapi AppDirectory $projectPath
& $nssm set fems_fastapi AppStdout "$projectPath\logs\service.log"
& $nssm set fems_fastapi AppStderr "$projectPath\logs\error.log"
& $nssm set fems_fastapi AppRotateFiles 1
& $nssm set fems_fastapi Start SERVICE_AUTO_START

# .env 환경변수 로드
Get-Content "$projectPath\.env" | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.*)$") {
        & $nssm set fems_fastapi AppEnvironmentExtra "+$($matches[1])=$($matches[2])"
    }
}

# 로그 폴더 생성
New-Item -ItemType Directory -Force -Path "$projectPath\logs"

& $nssm start fems_fastapi

Write-Host "완료! 서비스가 시작되었습니다."
Write-Host "상태 확인: & '$nssm' status fems_fastapi"
