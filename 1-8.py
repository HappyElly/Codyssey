# mars_mission_computer.py >> 파일명 중복
# 1-8

import random
import time
import json
import platform
import os
import subprocess

# 더미 센서 클래스
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    # 랜덤 숫자 생성
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    # 랜덤 숫자 반환
    def get_env(self):
        return self.env_values

# 미션 컴퓨터 클래스
class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.ds = DummySensor()

    def get_sensor_data(self):
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env() # 데이터 가공 주의
            print(json.dumps(self.env_values, indent=2, ensure_ascii=False))
            time.sleep(5)

    def get_mission_computer_info(self):
        total_gb = None
        try:
            # 윈도우 메모리 정보 가져오기
            out = subprocess.run(
                ['wmic', 'OS', 'get', 'TotalVisibleMemorySize', '/value'],
                capture_output=True, text=True, check=True
            ).stdout
            for line in out.splitlines():
                if 'TotalVisibleMemorySize' in line:
                    total_kb = int(line.split('=')[1].strip())
                    total_gb = round(total_kb / 1024 / 1024, 2)  # GB 단위 변환
        except Exception:
            pass

        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'cpu_type': platform.processor(),
            'cpu_cores': os.cpu_count(),
            'memory_total_gb': total_gb
        }
        print(json.dumps(info, indent=2, ensure_ascii=False))

    def get_mission_computer_load(self):
        cpu_percent = None
        mem_percent = None
        try:
            # 윈도우 CPU 사용량 가져오기
            out = subprocess.run(
                ['wmic', 'cpu', 'get', 'loadpercentage', '/value'],
                capture_output=True, text=True, check=True
            ).stdout
            for line in out.splitlines():
                if 'LoadPercentage' in line:
                    cpu_percent = float(line.split('=')[1].strip())
        except Exception:
            pass

        try:
            # 윈도우 메모리 사용량 가져오기
            out = subprocess.run(
                ['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/value'],
                capture_output=True, text=True, check=True
            ).stdout
            vals = {}
            for line in out.splitlines():
                if '=' in line:
                    k, v = line.split('=', 1)
                    vals[k.strip()] = int(v.strip())
            total_mb = vals.get('TotalVisibleMemorySize')
            free_mb = vals.get('FreePhysicalMemory')
            if total_mb and free_mb:
                mem_percent = round(100.0 * (1 - (free_mb / total_mb)), 1)
        except Exception:
            pass

        load = {
            'cpu_usage_percent': cpu_percent,
            'memory_usage_percent': mem_percent
        }
        print(json.dumps(load, indent=2, ensure_ascii=False))

if __name__ == '__main__': # 파일 직접 실행 시 코드 실행, import 될때는 시행 X
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

