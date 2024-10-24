#!/usr/bin/env python3
import sys
import subprocess
import os
import re
import shutil
import json
from pathlib import Path
import argparse
from collections import defaultdict
from datetime import datetime
from tqdm import tqdm

# Previous imports and RTL_SCRIPTS definition remain the same...

class ProcessingStats:
    def __init__(self):
        self.files_processed = 0
        self.files_modified = 0
        self.tags_modified = defaultdict(int)
        self.scripts_found = defaultdict(int)
        self.script_by_field = defaultdict(lambda: defaultdict(int))
        self.errors = []
        
    def to_report(self):
        """Generate a detailed report of processing statistics"""
        report = []
        report.append("\n=== Processing Report ===")
        report.append(f"Files processed: {self.files_processed}")
        report.append(f"Files modified: {self.files_modified}")
        
        if self.tags_modified:
            report.append("\nModified Tags Count:")
            for tag, count in sorted(self.tags_modified.items()):
                report.append(f"  {tag}: {count}")
        
        if self.scripts_found:
            report.append("\nRTL Scripts Found:")
            for script, count in sorted(self.scripts_found.items()):
                report.append(f"  {script}: {count} occurrences")
            
            report.append("\nScripts by Field:")
            for field, scripts in sorted(self.script_by_field.items()):
                report.append(f"\n  {field}:")
                for script, count in sorted(scripts.items()):
                    report.append(f"    {script}: {count}")
        
        if self.errors:
            report.append("\nErrors Encountered:")
            for error in self.errors:
                report.append(f"  - {error}")
        
        return "\n".join(report)

def create_backup(file_path, backup_dir):
    """Create a backup of the file with metadata preservation"""
    try:
        # Create backup directory if it doesn't exist
        backup_dir = Path(backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamp-based subdirectory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = backup_dir / timestamp
        backup_subdir.mkdir(exist_ok=True)
        
        # Preserve relative path structure
        rel_path = file_path.resolve().relative_to(Path.cwd())
        backup_path = backup_subdir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file with metadata preservation
        shutil.copy2(file_path, backup_path)
        
        # Create metadata file
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
    
    # List available backups
    backups = sorted([d for d in backup_dir.iterdir() if d.is_dir()])
    if not backups:
        print("No backups found.")
        return False
    
    if timestamp:
        # Restore specific backup
        backup_path = backup_dir / timestamp
        if not backup_path.exists():
            print(f"Backup {timestamp} not found.")
            return False
    else:
        # Restore most recent backup
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

# Modified process_folder function
def process_folder(folder_path, remove_str=None, reverse_rtl=False, reverse_tags=False, 
                  dry_run=False, backup_dir=None):
    """Process all audio files in the given folder with progress tracking"""
    folder = Path(folder_path)
    if not folder.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    stats = ProcessingStats()
    detector = RTLScriptDetector(stats)
    
    # Get all audio files
    audio_extensions = {'.mp3', '.ogg', '.flac', '.m4a', '.wav', '.wma'}
    audio_files = list(folder.rglob("*.*"))  # Using rglob for recursive search
    audio_files = [f for f in audio_files if f.suffix.lower() in audio_extensions]
    
    if not audio_files:
        print(f"No audio files found in {folder_path}")
        return
    
    # Create progress bar
    pbar = tqdm(audio_files, desc="Processing files", unit="file")
    
    for file_path in pbar:
        try:
            stats.files_processed += 1
            pbar.set_description(f"Processing: {file_path.name}")
            
            # Create backup if requested and not in dry run mode
            if backup_dir and not dry_run:
                if not create_backup(file_path, backup_dir):
                    stats.errors.append(f"Backup failed for {file_path}")
                    continue
            
            # Process the file
            changes_made = process_single_file(file_path, remove_str, reverse_rtl, 
                                            reverse_tags, dry_run, detector, stats)
            
            if changes_made:
                stats.files_modified += 1
                
        except Exception as e:
            error_msg = f"Error processing {file_path.name}: {str(e)}"
            stats.errors.append(error_msg)
            pbar.write(error_msg)
    
    # Print final report
    print(stats.to_report())

# Add visualization function
def create_script_distribution_visualization(stats):
    """Create a text-based visualization of script distribution"""
    if not stats.scripts_found:
        return "No RTL scripts found."
    
    total = sum(stats.scripts_found.values())
    max_bar_length = 40
    
    viz = ["Script Distribution:", "-" * 50]
    
    for script, count in sorted(stats.scripts_found.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        bar_length = int((count / total) * max_bar_length)
        bar = "█" * bar_length
        viz.append(f"{script:15} {bar} {percentage:5.1f}% ({count})")
    
    return "\n".join(viz)

# Modified main function to include new options
def main():
    parser = argparse.ArgumentParser(
        description="Process audio files: reverse RTL scripts and/or remove specified strings in filenames and tags"
    )
    parser.add_argument("folder", help="Path to folder containing audio files")
    parser.add_argument("--remove", help="String to remove from filenames")
    parser.add_argument("--reverse-rtl", action="store_true", help="Reverse RTL parts in filenames")
    parser.add_argument("--reverse-tags", action="store_true", help="Reverse RTL parts in ID3 tags")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually changing files")
    parser.add_argument("--backup-dir", help="Create backups in specified directory before modifications")
    parser.add_argument("--restore-backup", help="Restore from backup (specify timestamp or leave empty for most recent)")
    
    args = parser.parse_args()
    
    if args.restore_backup is not None:
        return restore_from_backup(args.backup_dir, args.restore_backup)
    
    if not any([args.remove, args.reverse_rtl, args.reverse_tags]):
        parser.error("At least one operation (--remove, --reverse-rtl, or --reverse-tags) must be specified")
    
    try:
        stats = process_folder(
            args.folder, args.remove, args.reverse_rtl, args.reverse_tags,
            args.dry_run, args.backup_dir
        )
        print("\nScript Distribution Visualization:")
        print(create_script_distribution_visualization(stats))
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

# Rest of the code remains the same...
