"""
RTL text processing utilities
"""

import re
from .script_definitions import RTL_SCRIPTS

def build_rtl_pattern():
    """Build regex pattern for all RTL ranges"""
    ranges_pattern = ''.join([
        f'{start}-{end}'
        for _, *ranges in RTL_SCRIPTS
        for start, end in ranges
    ])
    return f'[{ranges_pattern}]+'

def reverse_rtl_parts(text, stats=None):
    """Find RTL substrings and reverse them while maintaining other text"""
    if not text:
        return text
    
    if stats:
        stats.count_characters(text)
    
    pattern = re.compile(build_rtl_pattern())
    segments = []
    last_end = 0
    
    for match in pattern.finditer(text):
        if match.start() > last_end:
            segments.append((text[last_end:match.start()], False))
        segments.append((match.group()[::-1], True))
        last_end = match.end()
    
    if last_end < len(text):
        segments.append((text[last_end:], False))
    
    return ''.join(segment for segment, _ in segments)
