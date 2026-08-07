PROJECT = {
    "settings": {
        "tempo": 120,
        "time_signature": {
            "numerator": 4,
            "denominator": 4
        }
    },

    "track_order": [
        "track_001"
    ],

    "tracks": {
        "track_001": {
            "id": "track_001",
            "name": "Track 1",
            "type": "midi",
            "muted": False,
            "solo": False,
            "armed": False,

            "clips": {
                "clip_001": {
                    "id": "clip_001",
                    "start": 0,
                    "length": 16,

                    "notes": [
                        {
                            "pitch": 60,
                            "start": 0,
                            "duration": 1,
                            "velocity": 100,
                            "effects": [
                                {

                                },
                            ]
                        }
                    ]
                }
            }
        }
    }
}

UI = {
    "window_layout": {
        ...
    },
}