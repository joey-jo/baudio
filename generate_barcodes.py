#!/usr/bin/env python3
"""
바코드 이미지 생성 스크립트
000부터 099까지의 바코드를 한 장의 이미지에 생성합니다.

사용법:
  python3 generate_barcodes.py

생성된 바코드 이미지는 barcodes_000-099.png 파일로 저장됩니다.
"""

import os
import sys
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("오류: Pillow 패키지가 설치되지 않았습니다.")
    print("\n다음 명령어로 패키지를 설치해주세요:")
    print("  pip3 install Pillow")
    sys.exit(1)

try:
    from barcode import Code128
    from barcode.writer import ImageWriter
except ImportError:
    print("오류: python-barcode 패키지가 설치되지 않았습니다.")
    print("\n다음 명령어로 패키지를 설치해주세요:")
    print("  pip3 install 'python-barcode[images]'")
    sys.exit(1)

def generate_barcode_image():
    # 000부터 099까지 바코드 생성
    start_id = 0
    end_id = 99
    total_count = end_id - start_id + 1
    
    print(f"000부터 099까지 총 {total_count}개의 바코드를 생성합니다...\n")
    
    # 바코드 이미지들을 저장할 리스트
    barcode_images = []
    barcode_width = 0
    barcode_height = 0
    
    # 각 바코드 생성
    for i in range(start_id, end_id + 1):
        barcode_id = f"{i:03d}"  # 000, 001, 002, ..., 100 형식
        
        try:
            # Code128 바코드 생성
            code = Code128(barcode_id, writer=ImageWriter())
            
            # 메모리에 바코드 이미지 생성
            buffer = BytesIO()
            code.write(buffer, options={
                'format': 'PNG',
                'module_width': 0.5,
                'module_height': 15,
                'quiet_zone': 6,
                'font_size': 10,
                'text_distance': 3,
                'background': 'white',
                'foreground': 'black',
            })
            
            # PIL Image로 변환
            buffer.seek(0)
            img = Image.open(buffer)
            barcode_images.append((barcode_id, img))
            
            # 첫 번째 이미지의 크기를 기준으로 사용
            if barcode_width == 0:
                barcode_width, barcode_height = img.size
            
            if (i - start_id + 1) % 10 == 0:
                print(f"진행 중... {i - start_id + 1}/{total_count}")
        except Exception as e:
            print(f"✗ {barcode_id} 생성 실패: {e}")
    
    print(f"\n바코드 이미지들을 하나로 합치는 중...")
    
    # 그리드 레이아웃 설정 (10열로 배치)
    cols = 10
    rows = (total_count + cols - 1) // cols  # 올림 계산
    
    # 각 바코드 간 간격
    padding = 10
    
    # 전체 이미지 크기 계산
    total_width = cols * (barcode_width + padding) - padding
    total_height = rows * (barcode_height + padding) - padding
    
    # 전체 이미지 생성 (흰색 배경)
    combined_image = Image.new('RGB', (total_width, total_height), 'white')
    
    # 각 바코드를 그리드에 배치
    for idx, (barcode_id, img) in enumerate(barcode_images):
        row = idx // cols
        col = idx % cols
        
        x = col * (barcode_width + padding)
        y = row * (barcode_height + padding)
        
        combined_image.paste(img, (x, y))
    
    # 이미지 저장 (루트 디렉토리에 저장)
    output_filename = 'barcodes_000-099.png'
    combined_image.save(output_filename, 'PNG', dpi=(300, 300))
    
    print(f"\n✓ 완료! {output_filename} 파일이 생성되었습니다.")
    print(f"  크기: {total_width}x{total_height} 픽셀")
    print(f"  레이아웃: {rows}행 x {cols}열")

if __name__ == '__main__':
    generate_barcode_image()

