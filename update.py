import subprocess
import sys

def run(script: str) -> None:
    print(f"\n{'='*40}")
    print(f"Running {script}...")
    print('='*40)
    result = subprocess.run([sys.executable, script], check=True)
    
def main() -> None:
    run("get_list.py")
    run("csv2path.py")
    run("download.py")
    run("radar.py")

if __name__ == "__main__":
    main()