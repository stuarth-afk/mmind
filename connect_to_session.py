import os

def main():
    session_name = "tmux_main"  # Replace with the actual session name

    # Connect to the tmux session
    os.system(f"tmux attach-session -t {session_name}")

if __name__ == "__main__":
    main()

