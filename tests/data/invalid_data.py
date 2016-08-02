INVALID_IDS = {"bad_id_type": 42}

UNKNOWN_ID = "one_eyed_drunken_pirate"

INVALID_CONTEXTS = {
    "invalid_context_missing_type_key": {
        "context": {
            "presence": {
                "typo": "enum"
            },
            "lightIntensity": {
                "type": "continuous"
            },
            "lightbulbColor": {
                "type": "enum"
            }
        },
        "output": ["lightbulbColor"],
        "time_quantum": 100
    },
    "invalid_context_nonjsonserializable": {
        "context": {("1", "2", "3")},
        "output": ["lightbulbColor"],
        "time_quantum": 100
    }
}

INVALID_OUTPUTS = {"no_output": None,
                   "output_not_in_the_model": ["beerBrand"]}

UNDEFINED_KEY = {"none": None,
                 "empty_string": "",
                 "empty_dict": {},
                 "empty_list": []}

INVALID_TIME_QUANTA = {"negative_tq": -42,
                       "null_tq": 0}

INVALID_OPS_SET = {
    "incomplete_first_op": [
        {
            "timestamp": 1458741231,
            "diff": {
                "presence": "player",
                "lightIntensity": 0.5,
            }
        }
    ],
    "invalid_operation": [
        {
            "timestamp": 1458741230,
            "diff": {
                "tz": "+02:00",
                "presence": "occupant",
                "bananaIntensity": 1,
                "lightbulbColor": "#ffffff"
            }
        }
    ],
    "unexpected_time_property": [
        {
            "time_of_day": 0.5,
            "day_of_week": 5,
            "diff": {
                "presence": "occupant",
                "lightIntensity": 1,
                "lightbulbColor": "#ffffff"
            }
        }
    ],
    "dict_operations": {
        "time_of_day": 0.5,
        "day_of_week": 5,
        "diff": {
            "presence": "occupant",
            "lightIntensity": 1,
            "lightbulbColor": "#ffffff"
        }
    }
}
