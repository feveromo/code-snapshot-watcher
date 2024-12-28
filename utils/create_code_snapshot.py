import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
import difflib

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def get_gitignore_spec():
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        return None
        
    with open(gitignore_path) as f:
        spec = PathSpec.from_lines(GitWildMatchPattern, f.readlines())
    return spec

def create_code_snapshot(changed_file=None, old_content='', new_content='', output_file='full_code_snapshot.txt'):
    if changed_file is None:
        return
        
    gitignore_spec = get_gitignore_spec()
    snapshot_content = []
    colored_content = []
    
    # Skip if matches gitignore
    rel_path = changed_file.relative_to(Path().resolve())
    if gitignore_spec and gitignore_spec.match_file(str(rel_path)):
        return
        
    # Skip binary files
    if changed_file.suffix.lower() in {'.exe', '.dll', '.pyc', '.pyo'}:
        return
        
    header = f"\n{'='*80}\nFile: {rel_path}\n{'='*80}\n"
    snapshot_content.append(header)
    colored_content.append(header)
    
    # Generate diff for changed lines only
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    diff = list(difflib.unified_diff(old_lines, new_lines, n=2, lineterm=''))  # n=2 for 2 lines of context
    
    # If there are changes, add them to the snapshot
    if diff:
        changes_header = "\nChanges:\n"
        snapshot_content.append(changes_header)
        colored_content.append(changes_header)
        in_hunk = False
        for line in diff[2:]:  # Skip the first two lines of unified diff
            if line.startswith('@@'):
                in_hunk = True
                snapshot_content.append(f"\n{line}\n")
                colored_content.append(f"\n{Colors.CYAN}{line}{Colors.RESET}\n")
            elif in_hunk:
                if line.startswith('+'):
                    snapshot_content.append(line)
                    colored_content.append(f"{Colors.GREEN}{line}{Colors.RESET}")
                elif line.startswith('-'):
                    snapshot_content.append(line)
                    colored_content.append(f"{Colors.RED}{line}{Colors.RESET}")
                elif line.startswith(' '):
                    snapshot_content.append(f" {line[1:]}")
                    colored_content.append(f"{Colors.WHITE} {line[1:]}{Colors.RESET}")
    
    # Write plain text to file
    mode = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, mode, encoding='utf-8') as f:
        f.write('\n'.join(snapshot_content))
    
    # Print colored output to terminal
    print('\n'.join(colored_content))
    print(f"\nUpdated snapshot at: {output_file}")

if __name__ == "__main__":
    create_code_snapshot() 