#!/bin/bash

# 바코드 오디오 플레이어 실행 스크립트

PORT=8000

echo "바코드 오디오 플레이어를 시작합니다..."
echo "포트: $PORT"
echo ""
echo "브라우저에서 http://localhost:$PORT 로 접속하세요."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

# Python 3가 설치되어 있는지 확인
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m http.server $PORT
else
    echo "오류: Python이 설치되어 있지 않습니다."
    exit 1
fi

