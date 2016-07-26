VALID_ID = "one_legged_rainbow_unicorn"
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
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "time_quantum": VALID_TQ
}
