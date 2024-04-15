nodeData = [
    {
        "name": "Fish",
        "left": "1246px",
        "top": "353px",
        "states": [
            {
                "name": "zero",
                "probability": 0.2
            },
            {
                "name": "low",
                "probability": 0
            },
            {
                "name": "medium",
                "probability": 0
            },
            {
                "name": "high",
                "probability": 0
            },
            {
                "name": "zero",
                "probability": 0.2
            }
        ],
        "children": []
    },
    {
        "name": "Cover",
        "left": "717px",
        "top": "444px",
        "states": [
            {
                "name": "zero",
                "probability": 1
            },
            {
                "name": "low",
                "probability": 0.25
            },
            {
                "name": "medium",
                "probability": 0.01
            },
            {
                "name": "high",
                "probability": 0.5
            }
        ],
        "children": [
            "Fish"
        ]
    },
    {
        "name": "Migration",
        "left": "689px",
        "top": "107px",
        "states": [
            {
                "name": "zero",
                "probability": 0.95
            },
            {
                "name": "low",
                "probability": 0.5
            },
            {
                "name": "medium",
                "probability": 0.25
            },
            {
                "name": "high",
                "probability": 0
            }
        ],
        "children": [
            "Fish"
        ]
    },
    {
        "name": "Barrier",
        "left": "62px",
        "top": "112px",
        "states": [
            {
                "name": "none",
                "probability": 0.3
            },
            {
                "name": "some",
                "probability": 0.5
            },
            {
                "name": "many",
                "probability": 0.2
            },
            {
                "name": "huge",
                "probability": 0.2
            }
        ],
        "children": [
            "Migration"
        ]
    },
    {
        "name": "Discharge",
        "left": "72px",
        "top": "441px",
        "states": [
            {
                "name": "zero",
                "probability": 0.1
            },
            {
                "name": "low",
                "probability": 0.4
            },
            {
                "name": "medium",
                "probability": 0.4
            },
            {
                "name": "high",
                "probability": 0.1
            }
        ],
        "children": [
            "Cover"
        ]
    }
]



   