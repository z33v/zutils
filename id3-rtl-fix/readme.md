# Audio File RTL Script Reversal

A Python utility for handling Right-to-Left (RTL) scripts in audio file metadata and filenames. This tool ensures proper text display in devices and players with limited RTL language support.

## Purpose

Many portable music players, DIY audio devices, and simple displays have limited or no support for Right-to-Left (RTL) languages such as Hebrew, Arabic, and Syriac. This can result in garbled or incorrectly displayed text when playing music with metadata in these languages. Common affected devices include:

- SanDisk Clip series players
- DIY music players with basic LCD displays
- Car stereos with simple text displays
- Older MP3 players
- E-ink displays
- Basic LED matrices

This utility addresses these issues by:
1. Reversing RTL script segments in filenames and metadata
2. Preserving non-RTL text (English, numbers, etc.)
3. Handling mixed-script content appropriately
4. Supporting multiple audio formats
5. Creating backups before modifications

## Features

- **Multiple RTL Script Support:**
  - Hebrew (including presentation forms)
  - Arabic (including supplements)
  - Syriac
  - Thaana (Maldivian)
  - N'Ko (West African)
  - Other historical RTL scripts

- **Audio Format Support:**
  - MP3 (ID3v2)
  - OGG/FLAC (Vorbis Comments)
  - M4A/MP4 (Apple Tags)
  - WAV
  - WMA

- **Comprehensive Tag Handling:**
  - Basic metadata (title, artist, album)
  - Extended fields (composer, conductor, etc.)
  - Comments and descriptions
  - Lyrics (synced and unsynced)

- **Safety Features:**
  - Dry-run mode
  - Automatic backups
  - Detailed processing reports
  - Script distribution visualization

## Installation

```bash
# Clone the repository
git https://github.com/z33v/zutils/tree/main/id3-rtl-fix

# Install dependencies (Optional, software can sort by itself)
pip install mutagen tqdm
```

## Usage

Basic usage:
```bash
# Reverse RTL scripts in filenames
./id3-rtl-fix.py --reverse-rtl /path/to/folder

# Reverse RTL scripts in tags
./id3-rtl-fix.py --reverse-tags /path/to/folder

# Remove string from filenames and reverse RTL scripts
./id3-rtl-fix.py --remove "string_to_remove" --reverse-rtl --reverse-tags /path/to/folder

# Test changes without applying them
./id3-rtl-fix.py --dry-run --reverse-rtl --reverse-tags /path/to/folder

# Create backups before processing
./id3-rtl-fix.py --backup-dir ./backups --reverse-rtl --reverse-tags /path/to/folder
```

## Example Output

```
Character Distribution (by script):
------------------------------------------------------------
Hebrew          ████████████████████ 50.0% (1,234 chars)
Arabic          ███████████████      37.5% (945 chars)
Syriac          ████                 10.0% (251 chars)
Non-RTL         █                     2.5% (63 chars)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Mutagen library developers
- The Python community
- All contributors and users who help improve this tool

## Support

If you encounter any issues or have questions:
1. Check the existing issues
2. Open a new issue with a clear description
3. Include sample files if possible (without sensitive content)
