import subprocess

def main():
    script_path = "main.py"  # Replace with the name of your main script
    session_name = f"tmux_{script_path.replace('.py', '')}"
    
    # Create a new tmux session
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name])
    
    # Run the main script in the tmux session
    subprocess.run(["tmux", "send-keys", "-t", session_name, f"python {script_path}", "Enter"])

    print(f"Script '{script_path}' is running in tmux session '{session_name}'")

if __name__ == "__main__":
    main()

