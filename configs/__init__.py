import yaml

with open("configs/prod.yml", "r") as f:
    config = yaml.safe_load(f)
