INVALID_IDS = {"bad_id_type": 42}

INVALID_CONTEXTS = {"no_context": None,
                    "empty_context": {},
                    "invalid_context_type": {
                        "presence": {
                            "type": "chair"
                        },
                        "lightIntensity": {
                            "type": "continuous"
                        },
                        "lightbulbColor": {
                            "type": "enum"
                        }
                    },
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
                    }}

INVALID_OUTPUTS = {"no_output": None,
                   "output_not_in_the_model": ["beerBrand"]}

UNDEFINED_KEY = {"none": None,
                 "empty_string": "",
                 "empty_dict": {}}

INVALID_TIME_QUANTA = {"negative_tq": -42,
                       "null_tq": 0}
                       # "float_tq": 3.141592}
