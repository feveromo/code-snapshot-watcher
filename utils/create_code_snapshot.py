import os
from pathlib import Path
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
import difflib

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
    
    # Skip if matches gitignore
    rel_path = changed_file.relative_to(Path().resolve())
    if gitignore_spec and gitignore_spec.match_file(str(rel_path)):
        return
        
    # Skip binary files
    if changed_file.suffix.lower() in {'.exe', '.dll', '.pyc', '.pyo'}:
        return
        
    snapshot_content.append(f"\n{'='*80}\n")
    snapshot_content.append(f"File: {rel_path}\n")
    snapshot_content.append(f"{'='*80}\n")
    
    # Generate diff for all files
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=''))
    
    if diff:
        snapshot_content.append("\nChanges:\n")
        for line in diff[2:]:  # Skip the first two lines of unified diff
            if line.startswith('+'):
                snapshot_content.append(f"{line}")  # Already has + prefix
            elif line.startswith('-'):
                snapshot_content.append(f"{line}")  # Already has - prefix
            elif line.startswith('@@'):
                snapshot_content.append(f"\n{line}\n")  # Section header
            else:
                snapshot_content.append(f" {line[1:]}")  # Remove the space prefix
    
    # Append to the snapshot file instead of overwriting
    mode = 'a' if os.path.exists(output_file) else 'w'
    with open(output_file, mode, encoding='utf-8') as f:
        f.write('\n'.join(snapshot_content))
    
    print(f"Updated snapshot at: {output_file}")

if __name__ == "__main__":
    create_code_snapshot() 