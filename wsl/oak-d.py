import subprocess
import time

def get_attached_busids():
    try:
        output = subprocess.check_output('usbipd list', shell=True, encoding='utf-8')
        lines = output.splitlines()
        attached = [line.split()[0] for line in lines if 'Attached' in line]
        return attached
    except subprocess.CalledProcessError as e:
        print(f"Error fetching attached list: {e}")
        return []

while True:
    shared_output = subprocess.check_output('usbipd list', shell=True, encoding='utf-8')
    attached_busids = get_attached_busids()

    for row in shared_output.splitlines():
        if 'Movidius MyriadX' in row or 'Luxonis Device' in row:
            parts = row.strip().split()
            busid = parts[0] if parts else None
            if busid and busid not in attached_busids:
                try:
                    out = subprocess.check_output(f'usbipd attach --wsl --busid {busid}', shell=True, encoding='utf-8')
                    print(out)
                    print(f'✅ Attached MyriadX on bus {busid}')
                except subprocess.CalledProcessError as e:
                    print(f'❌ Attach failed: {e}')
    time.sleep(1)
