import toml
import glob
import os
import json

def create_dirs(path):
  try:
    os.makedirs(path)
  except OSError:
      print(f"failed to create {path}")
  else:
      print(f"created {path}")

def dump_toml(path, obj):
  with open(path, 'w') as f:
    toml.dump(obj, f)

def dump_json(path, obj):
  with open(path, 'w') as f:
    json.dump(obj, f, indent=2)

create_dirs("generated")

global_config = toml.load("global.toml")

print(global_config)

for filepath in glob.iglob('crates/*.toml'):
  print(filepath)
  crate_config = toml.load(filepath)
  print(crate_config)
  all_config = {**global_config, **crate_config}
  print(all_config)
  name = filepath.split("/")[1].split(".toml")[0]
  print(name)
  root = f"generated/{name}"
  print(root)
  create_dirs(root)
  package = {
    "name": name,
    "authors": [f"{author['name']} <{author['email']}>" for author in global_config["author"]],
    "keywords": all_config["keywords"]
  }
  bbin = {
    "name": "example",
    "path": "src/example.rs"
  }
  cargo_toml = {
    "package": package,    
    #"bin": bbin
  }
  print(cargo_toml)
  dump_json(f"{root}/Cargo.json", cargo_toml)
  dump_toml(f"{root}/Cargo.toml", cargo_toml)
  