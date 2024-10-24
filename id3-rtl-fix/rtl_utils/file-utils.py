"""
File operation utilities including backup and restore functionality
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def create_backup(file_path, backup_dir):
    """Create a backup of the file with metadata preservation"""
    try:
        backup_dir = Path(backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = backup_dir / timestamp
        backup_subdir.mkdir(exist_ok=True)
        
        rel_path = file_path.resolve().relative_to(Path.cwd())
        backup_path = backup_subdir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_path)
        
        metadata = {
            "original_path": str(file_path),
            "backup_time": timestamp,
            "file_size": file_path.stat().st_size,
        }
        metadata_path = backup_path.with_suffix(backup_path.suffix + ".meta")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error creating backup of {file_path}: {str(e)}")
        return False

def restore_from_backup(backup_dir, timestamp=None):
    """Restore files from backup"""
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        print("No backups found.")
        return False
    
    backups = sorted([d for d in backup_dir.iterdir() if d.is_dir()])
    if not backups:
        print("No backups found.")
        return False
    
    if timestamp:
        backup_path = backup_dir / timestamp
        if not backup_path.exists():
            print(f"Backup {timestamp} not found.")
            return False
    else:
        backup_path = backups[-1]
    
    try:
        print(f"Restoring from backup: {backup_path.name}")
        for meta_file in backup_path.rglob("*.meta"):
            with open(meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            original_path = Path(metadata["original_path"])
            backup_file = meta_file.with_suffix("")
            
            if backup_file.exists():
                original_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, original_path)
                print(f"Restored: {original_path}")
        
        return True
    except Exception as e:
        print(f"Error restoring from backup: {str(e)}")
        return False
