#!/usr/bin/env python3
"""
Audio File RTL Script Reversal
-----------------------------
Ensures proper RTL script display in audio players with limited RTL support
by reversing RTL text segments in filenames and audio metadata.

MIT License
Copyright (c) 2024 Audio File RTL Reversal Contributors
"""

import sys
import os
import argparse
from pathlib import Path

# First, import our library checker
from rtl_utils.library_checker import ensure_libraries_installed

# Ensure required libraries are installed before importing them
ensure_libraries_installed()

# Now we can safely import external libraries
from mutagen import File
from mutagen.easyid3 import EasyID3
from tqdm import tqdm

# Import the rest of our utilities
from rtl_utils.text_processor import reverse_rtl_parts
from rtl_utils.file_utils import create_backup, restore_from_backup
from rtl_utils.tag_mappings import TAG_MAPPINGS
from rtl_utils.stats_collector import ScriptStats

def process_audio_tags(file_path, audio, format_type, reverse_rtl=False, dry_run=False, stats=None):
    """Process tags for a specific audio format"""
    changes_made = False
    tag_mapping = TAG_MAPPINGS[format_type]
    
    for category, tags in tag_mapping.items():
        for tag in tags:
            if tag in audio:
                values = audio[tag]
                if not isinstance(values, list):
                    values = [values]
                
                new_values = []
                for value in values:
                    if isinstance(value, (bytes, bytearray)):
                        try:
                            str_value = value.decode('utf-8')
                        except UnicodeDecodeError:
                            continue
                    else:
                        str_value = str(value)
                    
                    new_value = reverse_rtl_parts(str_value, stats)
                    if new_value != str_value:
                        if dry_run:
                            print(f"Would update {tag} ({category}): {str_value} → {new_value}")
                        else:
                            print(f"Updated {tag} ({category}): {str_value} → {new_value}")
                            changes_made = True
                            if stats:
                                stats.tags_modified[tag] += 1
                    new_values.append(new_value)
                
                if changes_made and not dry_run:
                    audio[tag] = new_values
    
    if changes_made and not dry_run:
        try:
            audio.save()
        except Exception as e:
            if stats:
                stats.errors.append(f"Error saving tags for {file_path}: {str(e)}")
            return False
    
    return changes_made

def process_file(file_path, remove_str=None, reverse_rtl=False, reverse_tags=False, dry_run=False, stats=None):
    """Process a single audio file"""
    changes_made = False
    
    try:
        # Process filename if requested
        if remove_str or reverse_rtl:
            old_name = file_path.name
            new_name = old_name
            
            if remove_str:
                new_name = new_name.replace(remove_str, '')
            
            if reverse_rtl:
                new_name = reverse_rtl_parts(new_name, stats)
            
            if new_name != old_name:
                new_path = file_path.parent / new_name
                if dry_run:
                    print(f"Would rename: {old_name} → {new_name}")
                else:
                    file_path.rename(new_path)
                    file_path = new_path
                    print(f"Renamed: {old_name} → {new_name}")
                changes_made = True
        
        # Process tags if requested
        if reverse_tags:
            try:
                audio = EasyID3(file_path)
                format_type = 'ID3'
            except:
                audio = File(file_path)
                if audio is None:
                    if stats:
                        stats.errors.append(f"Unsupported format: {file_path}")
                    return changes_made
                
                if hasattr(audio, 'tags'):
                    if 'VORBIS' in str(type(audio.tags)):
                        format_type = 'VORBIS'
                    elif 'MP4' in str(type(audio.tags)):
                        format_type = 'APPLE'
                    else:
                        format_type = 'ID3'
                    
                    tag_changes = process_audio_tags(
                        file_path, audio.tags, format_type,
                        reverse_rtl, dry_run, stats
                    )
                    changes_made = changes_made or tag_changes
    
    except Exception as e:
        if stats:
            stats.errors.append(f"Error processing {file_path}: {str(e)}")
    
    return changes_made

def process_folder(folder_path, remove_str=None, reverse_rtl=False, reverse_tags=False, 
                  dry_run=False, backup_dir=None):
    """Process all audio files in the given folder"""
    folder = Path(folder_path)
    if not folder.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    stats = ScriptStats()
    
    # Get all audio files
    audio_extensions = {'.mp3', '.ogg', '.flac', '.m4a', '.wav', '.wma'}
    audio_files = list(folder.rglob("*.*"))  # Using rglob for recursive search
    audio_files = [f for f in audio_files if f.suffix.lower() in audio_extensions]
    
    if not audio_files:
        print(f"No audio files found in {folder_path}")
        return stats
    
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
            changes_made = process_file(
                file_path, remove_str, reverse_rtl, 
                reverse_tags, dry_run, stats
            )
            
            if changes_made:
                stats.files_modified += 1
                
        except Exception as e:
            error_msg = f"Error processing {file_path.name}: {str(e)}"
            stats.errors.append(error_msg)
            pbar.write(error_msg)
    
    return stats

def main():
    parser = argparse.ArgumentParser(
        description="Process audio files: reverse RTL scripts and/or remove specified strings "
                  "in filenames and tags"
    )
    parser.add_argument(
        "folder", 
        help="Path to folder containing audio files"
    )
    parser.add_argument(
        "--remove", 
        help="String to remove from filenames"
    )
    parser.add_argument(
        "--reverse-rtl",
        action="store_true",
        help="Reverse RTL parts in filenames"
    )
    parser.add_argument(
        "--reverse-tags",
        action="store_true",
        help="Reverse RTL parts in ID3 tags"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be done without actually changing files"
    )
    parser.add_argument(
        "--backup-dir", 
        help="Create backups in specified directory before modifications"
    )
    parser.add_argument(
        "--restore-backup", 
        help="Restore from backup (specify timestamp or leave empty for most recent)"
    )
    
    args = parser.parse_args()
    
    # Ensure required libraries are installed
    ensure_libraries_installed()
    
    if args.restore_backup is not None:
        return 0 if restore_from_backup(args.backup_dir, args.restore_backup) else 1
    
    if not any([args.remove, args.reverse_rtl, args.reverse_tags]):
        parser.error("At least one operation (--remove, --reverse-rtl, or --reverse-tags) "
                    "must be specified")
    
    try:
        stats = process_folder(
            args.folder, args.remove, args.reverse_rtl, args.reverse_tags,
            args.dry_run, args.backup_dir
        )
        print(stats.to_report())
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
