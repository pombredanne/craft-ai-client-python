VALID_ID = "one_legged_rainbow_unicorn"
VALID_CONTEXT = {
    "tz": {
        "type": "timezone"
    },
    "presence": {
        "type": "enum"
    },
    "lightIntensity": {
        "type": "continuous"
    },
    "lightbulbColor": {
        "type": "enum"
    }
}
VALID_OUTPUT = ["lightbulbColor"]
VALID_TQ = 100
VALID_MODEL = {
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "time_quantum": VALID_TQ
}

VALID_TIMESTAMP = 1458741230
VALID_OPERATIONS_SET = [
    {
        "timestamp": VALID_TIMESTAMP,
        "diff": {
            "tz": "+02:00",
            "presence": "occupant",
            "lightIntensity": 1,
            "lightbulbColor": "#ffffff"
        }
    },
    {
        "timestamp": 1458741231,
        "diff": {
            "presence": "player",
            "lightIntensity": 0.5,
        }
    },
    {
        "timestamp": 1458741232,
        "diff": {
            "presence": "none",
            "lightIntensity": 0,
        }
    },
    {
        "timestamp": 1458741242,
        "diff": {
            "presence": "occupant+player"
        }
    },
    {
        "timestamp": 1458741252,
        "diff": {
            "tz": "+01:00",
            "presence": "occupant",
            "lightIntensity": 0.8,
            "lightbulbColor": "#f56fff"
        }
    },
    {
        "timestamp": 1458741262,
        "diff": {
            "presence": "player",
            "lightIntensity": 0.5,
            "lightbulbColor": "#fff596"
        }
    }
]
