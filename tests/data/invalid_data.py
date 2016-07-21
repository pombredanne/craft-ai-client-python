INVALID_IDS = (("bad_id_type", 42),
               ("empty_id", ""),
               ("undefined_id", None))

INVALID_CONTEXTS = (("no_context", None),
                    ("empty_context", {}),
                    ("invalid_context_type", {
                        "presence": {
                            "type": "chair"
                        },
                        "lightIntensity": {
                            "type": "continuous"
                        },
                        "lightbulbColor": {
                            "type": "enum"
                        }
                    }),
                    ("invalid_context_missing_type_key", {
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
                    }))

INVALID_OUTPUTS = (("no_output", None),
                   ("output_not_in_the_model", ["beerBrand"]))

UNSPECIFIED_MODELS = (None,
                      "",
                      {})

INVALID_TIME_QUANTA = (("negative_tq", -42),
                       ("null_tq", 0),
                       ("high_tq", 4294967296),
                       ("float_tq", 3.141592))
