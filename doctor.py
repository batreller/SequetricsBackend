import subprocess
import shutil

def check_ffmpeg():
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"✅ FFmpeg found: {ffmpeg_path}")
        try:
            output = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
            print(output.decode().splitlines()[0])
        except Exception as e:
            print(f"⚠️ FFmpeg found but cannot run: {e}")
    else:
        print("❌ FFmpeg not found! Please install ffmpeg.")

def check_nvidia_gpu():
    try:
        output = subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT)
        lines = output.decode().splitlines()
        gpu_line = None
        for line in lines:
            if "GeForce" in line or "RTX" in line or "Tesla" in line or "Quadro" in line:
                gpu_line = line.strip()
                break
        if gpu_line:
            print(f"✅ NVIDIA GPU detected: {gpu_line}")
        else:
            print("✅ NVIDIA GPU detected, but name could not be determined.")
    except FileNotFoundError:
        print("ℹ️ nvidia-smi not found. NVIDIA GPU might not be present or drivers not installed.")
    except subprocess.CalledProcessError:
        print("⚠️ nvidia-smi returned an error. Check GPU drivers.")

def check_opencl():
    try:
        output = subprocess.check_output(["clinfo"], stderr=subprocess.STDOUT)
        devices_found = False
        for line in output.decode().splitlines():
            if "Device Name" in line:
                print(f"✅ OpenCL device found: {line.split(':',1)[1].strip()}")
                devices_found = True
        if not devices_found:
            print("ℹ️ OpenCL installed but no devices detected.")
    except FileNotFoundError:
        print("ℹ️ clinfo not found. Cannot check OpenCL devices.")
    except subprocess.CalledProcessError:
        print("⚠️ clinfo returned an error.")

if __name__ == "__main__":
    print("=== FFmpeg & GPU Health Check ===\n")
    check_ffmpeg()
    print("\n--- NVIDIA GPU ---")
    check_nvidia_gpu()
    print("\n--- OpenCL ---")
    check_opencl()
