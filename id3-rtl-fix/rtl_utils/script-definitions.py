"""
RTL script Unicode range definitions
"""

RTL_SCRIPTS = [
    # Modern scripts
    ('Hebrew', ('\u0590', '\u05FF'), ('\uFB1D', '\uFB4F')),
    ('Arabic', ('\u0600', '\u06FF'), ('\u0750', '\u077F'), ('\u08A0', '\u08FF'), 
             ('\uFB50', '\uFDFF'), ('\uFE70', '\uFEFF')),
    ('Syriac', ('\u0700', '\u074F'), ('\u0860', '\u086F')),
    ('Thaana', ('\u0780', '\u07BF')),
    ('NKo', ('\u07C0', '\u07FF')),
    ('Mandaic', ('\u0840', '\u085F')),
    # Ancient scripts
    ('Samaritan', ('\u0800', '\u083F')),
    ('Imperial Aramaic', ('\u10840', '\u1085F')),
    ('Phoenician', ('\u10900', '\u1091F')),
    ('Nabataean', ('\u10880', '\u108AF')),
    ('Lydian', ('\u10920', '\u1093F')),
    ('Meroitic', ('\u10980', '\u1099F'), ('\u109A0', '\u109FF')),
]
