VALID_ID = "one legged rainbow unicorn"
VALID_CONTEXT = {
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
    "model": {
        "context": VALID_CONTEXT,
        "output": VALID_OUTPUT,
        "time_quantum": VALID_TQ
    }
}
