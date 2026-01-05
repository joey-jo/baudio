// 전역 변수
let config = null;
let currentAudio = null;

// DOM 요소
const barcodeInput = document.getElementById('barcodeInput');
const statusDisplay = document.getElementById('statusDisplay');
const infoDisplay = document.getElementById('infoDisplay');

// config.json 로드
async function loadConfig() {
    try {
        const response = await fetch('config.json');
        if (!response.ok) {
            throw new Error('config.json을 불러올 수 없습니다');
        }
        config = await response.json();
    } catch (error) {
        console.error('설정 파일 로드 실패:', error);
        showError('설정 파일을 불러올 수 없습니다');
    }
}

// 정보 표시 (정상 상태)
function showInfo(message) {
    infoDisplay.textContent = message;
    infoDisplay.className = 'info-display info-normal';
}

// 오류 메시지 표시
function showError(message) {
    infoDisplay.textContent = message;
    infoDisplay.className = 'info-display info-error';
}

// 상태 업데이트
function updateStatus(status) {
    statusDisplay.textContent = status;
}

// 오디오 재생
function playAudio(audioPath, description) {
    // 이전 재생 중지
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }

    // 새 오디오 생성 및 재생
    currentAudio = new Audio(audioPath);
    
    currentAudio.addEventListener('loadstart', () => {
        updateStatus('로딩 중');
    });

    currentAudio.addEventListener('canplay', () => {
        updateStatus('재생 중');
        showInfo(description);
    });

    currentAudio.addEventListener('ended', () => {
        updateStatus('대기 중');
    });

    currentAudio.addEventListener('error', (e) => {
        updateStatus('대기 중');
        showError(`오디오 파일을 불러올 수 없습니다: ${audioPath}`);
        currentAudio = null;
    });

    currentAudio.play().catch((error) => {
        updateStatus('대기 중');
        showError(`오디오 재생 실패: ${error.message}`);
        currentAudio = null;
    });
}

// 바코드 처리
function processBarcode(barcode) {
    // 3자리 숫자로 정규화 (앞에서 3자리만 사용)
    const normalizedBarcode = barcode.slice(0, 3).padStart(3, '0');
    
    // config 확인
    if (!config || !config.mappings) {
        showError('설정이 로드되지 않았습니다');
        return;
    }

    const mapping = config.mappings[normalizedBarcode];
    
    if (!mapping) {
        showError(`알 수 없는 ID: ${normalizedBarcode}`);
        updateStatus('대기 중');
        return;
    }

    // 오디오 재생
    playAudio(mapping.file, mapping.description);
}

// 입력 이벤트 처리
barcodeInput.addEventListener('input', (e) => {
    const value = e.target.value;
    
    // 숫자만 추출
    const numbers = value.replace(/\D/g, '');
    
    // 입력 필드에 숫자만 표시
    if (value !== numbers) {
        e.target.value = numbers;
    }
    
    // 3자리 숫자가 입력되면 처리
    if (numbers.length >= 3) {
        const barcode = numbers.slice(0, 3);
        processBarcode(barcode);
        // 입력 필드 초기화
        e.target.value = '';
    }
});

// 포커스 유지
barcodeInput.addEventListener('blur', () => {
    setTimeout(() => {
        barcodeInput.focus();
    }, 0);
});

// 초기화
async function init() {
    await loadConfig();
    updateStatus('대기 중');
    barcodeInput.focus();
}

// 페이지 로드 시 초기화
window.addEventListener('DOMContentLoaded', init);

