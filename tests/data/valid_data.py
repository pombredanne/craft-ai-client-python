VALID_ID = "craft_ai_unit_test_agent_1"
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
VALID_CONFIGURATION = {
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "time_quantum": VALID_TQ
}

VALID_TIMESTAMP = 1458741230
VALID_OPERATIONS_SET = [
    {
        "timestamp": VALID_TIMESTAMP,
        "context": {
            "tz": "+02:00",
            "presence": "occupant",
            "lightIntensity": 1,
            "lightbulbColor": "#ffffff"
        }
    },
    {
        "timestamp": 1458741231,
        "context": {
            "presence": "player",
            "lightIntensity": 0.5,
        }
    },
    {
        "timestamp": 1458741232,
        "context": {
            "presence": "none",
            "lightIntensity": 0,
        }
    },
    {
        "timestamp": 1458741242,
        "context": {
            "presence": "occupant+player"
        }
    },
    {
        "timestamp": 1458741252,
        "context": {
            "tz": "+01:00",
            "presence": "occupant",
            "lightIntensity": 0.8,
            "lightbulbColor": "#f56fff"
        }
    },
    {
        "timestamp": 1458741262,
        "context": {
            "presence": "player",
            "lightIntensity": 0.5,
            "lightbulbColor": "#fff596"
        }
    }
]
