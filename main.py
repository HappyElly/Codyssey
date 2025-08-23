# 1-1

LOG_FILE = 'mission_computer_main.log'
REPORT_FILE = 'log_analysis.md'

log_lines = []

# 로그 파일 읽고 출력하기
try:
    with open(LOG_FILE, mode='r', encoding='utf-8', errors='replace') as log :
        for line in log:
            print(line, end='')
            log_lines.append(line)
except FileNotFoundError:
    print('[ERROR] 파일을 찾을 수 없습니다:')
except Exception :
    print("[ERROR] 알 수 없는 오류")

# Markdown 보고서 작성하기
with open(REPORT_FILE, 'w', encoding='utf-8') as report:
    report.write('# Mission Computer Log Analysis\n\n')
    for line in log_lines:
        report.write(line)