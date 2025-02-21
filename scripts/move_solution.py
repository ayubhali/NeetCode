import shutil
import subprocess
import questionary  # For interactive selection
from pathlib import Path

# Define project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
NEETCODE_DIR = ROOT_DIR / "NeetCode"
NEW_PROBLEMS_DIR = ROOT_DIR / "new_probs"
README_FILE = ROOT_DIR / "README.md"

# Define NeetCode topic folders
TOPIC_FOLDERS = [
    "0_Arrays_Hashing", "1_Stack", "2_Two_Pointers", "3_Binary_Search", "4_Sliding_Window",
    "5_Linked_List", "6_Trees", "7_Tries", "8_Backtracking", "9_Heap_Priority_Queue",
    "10_Intervals", "11_Greedy", "12_Advanced_Graphs", "13_Graphs",
    "14_1-DP", "15_2-DP", "16_Bit_Manipulation", "17_Math_Geometry"
]

# Ensure topic directories exist
for folder in TOPIC_FOLDERS:
    (NEETCODE_DIR / folder).mkdir(parents=True, exist_ok=True)

# Ensure new_probs directory exists
NEW_PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)

def list_new_problems():
    """List available Python files in new_probs."""
    return [f.name for f in NEW_PROBLEMS_DIR.glob("*.py")]

def move_solution():
    """Move new problem files to the correct topic folder."""
    print("\n🚀 **LeetCode Problem Organizer (By Topic)** 🚀\n")

    # Get list of new problems
    python_files = list_new_problems()

    if not python_files:
        print("✅ No new problems found in `new_probs/`.\n")
        return None, None

    for file_name in python_files:
        print(f"\n📌 Processing `{file_name}`...\n")

        # Ask user to select the topic folder
        topic = questionary.select(
            f"🔹 Select the topic for `{file_name}`:",
            choices=TOPIC_FOLDERS
        ).ask()

        source_file = NEW_PROBLEMS_DIR / file_name
        target_folder = NEETCODE_DIR / topic
        target_file = target_folder / file_name

        print(f"📂 Moving `{file_name}` to `{target_folder}`...")
        shutil.move(str(source_file), str(target_file))
        print("✅ File moved successfully!\n")

        # Update README
        update_readme(file_name.replace(".py", ""), topic)

    return True, True  # Placeholder return to signal changes were made

def update_readme(problem_name, topic):
    """Update README with solved problems."""
    if problem_name is None:
        return

    print("📝 Updating README.md...")
    with open(README_FILE, 'a') as f:
        github_url = f"https://github.com/yourusername/NeetCode/{topic}/{problem_name}.py"
        f.write(f"- [{problem_name}]({github_url}) - **Topic:** {topic}\n")

    print("✅ README.md updated.\n")

def git_operations():
    """Perform Git add, commit, and push."""
    print("🔄 Starting Git operations...")
    subprocess.run(["git", "add", "."], check=True)

    # Check if there are changes to commit
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("ℹ️ No changes to commit.\n")
        return

    subprocess.run(["git", "commit", "-m", "Auto update of solved problems"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Git operations completed.\n")

def main():
    moved, _ = move_solution()
    if moved:
        git_operations()

if __name__ == "__main__":
    main()
