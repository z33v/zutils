"""
Audio tag definitions and format mappings
"""

TAG_MAPPINGS = {
    # ID3 tags (MP3)
    'ID3': {
        'basic': [
            'title', 'artist', 'album', 'albumartist', 'composer',
            'genre', 'copyright', 'publisher', 'lyricist', 'conductor',
            'remixer', 'author', 'isrc', 'language', 'discsubtitle',
            'mood', 'version', 'script'
        ],
        'comments': [
            'comment', 'description'
        ],
        'lyrics': [
            'lyrics', 'unsyncedlyrics', 'syncedlyrics'
        ]
    },
    # Vorbis comments (OGG, FLAC)
    'VORBIS': {
        'basic': [
            'TITLE', 'ARTIST', 'ALBUM', 'ALBUMARTIST', 'COMPOSER',
            'GENRE', 'COPYRIGHT', 'PUBLISHER', 'LYRICIST', 'CONDUCTOR',
            'REMIXER', 'AUTHOR', 'ISRC', 'LANGUAGE', 'VERSION',
            'SUBTITLE', 'DISCSUBTITLE', 'MOOD'
        ],
        'comments': [
            'COMMENT', 'DESCRIPTION'
        ],
        'lyrics': [
            'LYRICS', 'UNSYNCEDLYRICS', 'SYNCEDLYRICS'
        ]
    },
    # Apple tags (M4A, MP4)
    'APPLE': {
        'basic': [
            '©nam', '©ART', '©alb', 'aART', '©wrt',
            '©gen', '©cpy', '©pub', '©lyr', '©con',
            'remix', '©aut', 'xid', '©lnd', 'subt',
            'mood', 'vers'
        ],
        'comments': [
            '©cmt', 'desc'
        ],
        'lyrics': [
            '©lyr'
        ]
    }
}
