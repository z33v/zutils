"""
Statistics collection and reporting utilities
"""

from collections import defaultdict
from .script_definitions import RTL_SCRIPTS

class ScriptStats:
    def __init__(self):
        self.files_processed = 0
        self.files_modified = 0
        self.tags_modified = defaultdict(int)
        self.scripts_found = defaultdict(int)
        self.script_by_field = defaultdict(lambda: defaultdict(int))
        self.characters_counted = defaultdict(int)
        self.errors = []
        
    def count_characters(self, text):
        """Count characters by script type"""
        for char in text:
            script_found = False
            for script_name, *ranges in RTL_SCRIPTS:
                if any(start <= char <= end for start, end in ranges):
                    self.characters_counted[script_name] += 1
                    script_found = True
                    break
            if not script_found:
                self.characters_counted["Non-RTL"] += 1
    
    def create_distribution_visualization(self):
        """Create a text-based visualization of script distribution"""
        if not self.characters_counted:
            return "No text analysis available."
        
        total_chars = sum(self.characters_counted.values())
        max_bar_length = 40
        
        viz = [
            "Character Distribution (by script):",
            "-" * 60
        ]
        
        # Sort by count, but ensure "Non-RTL" is last if present
        sorted_items = sorted(
            self.characters_counted.items(),
            key=lambda x: (x[0] == "Non-RTL", -x[1])
        )
        
        for script, count in sorted_items:
            percentage = (count / total_chars) * 100
            bar_length = int((count / total_chars) * max_bar_length)
            bar = "█" * bar_length
            viz.append(f"{script:15} {bar} {percentage:5.1f}% ({count:,} chars)")
        
        return "\n".join(viz)
    
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
        
        report.append("\n" + self.create_distribution_visualization())
        
        if self.errors:
            report.append("\nErrors Encountered:")
            for error in self.errors:
                report.append(f"  - {error}")
        
        return "\n".join(report)
