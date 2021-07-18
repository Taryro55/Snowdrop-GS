import json

config = {
    "Token": "ODMyNDAyMDg4NDExMzk4MTg2.YHjQ2w.1Sx4E_Q-NMhf_uuUcPyC4FKPT5Q",
    "GuildID": 661257524653195289,
    "ModID": 687376984443060229,
    "MemberID": 700463151178711131,
    "Toke": {
            "T": 861996789791850496,
            "A": 8619967
        }   
}

config = config[str('Toke')][str('A')]

print(config)