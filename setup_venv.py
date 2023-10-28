import os
import subprocess
import sys
import venv

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
        sys.exit(1)

def main():
    # Step 1: Create a virtual environment
    venv_dir = "mighty"

    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("Virtual environment exists.")

    # Step 2: Activate the virtual environment
    activate_script = "activate"
    
    if os.name == "nt":  # For Windows
        activate_script += ".bat"
        command = os.path.join(venv_dir, "Scripts", activate_script)
        run_command(f"cmd /k {command}")
    else:  # For macOS and Linux
        command = f". {os.path.join(venv_dir, 'bin', activate_script)}"
        run_command(command)

    # Step 3: Install dependencies from requirements.txt
    if os.path.exists("requirements.txt"):
        print("Installing dependencies...")
        run_command("pip install -r requirements.txt")
    else:
        print("requirements.txt not found.")
    
    print("Setup complete.")

if __name__ == "__main__":
    main()
