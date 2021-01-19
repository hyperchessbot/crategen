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
  authors = all_config.get("author", [{
    "name": "Joe Doe",
    "email": "joedoe@gmail.com",
  }])
  main_author = authors[0]
  vcss = all_config.get("vcs", [{
    "type": "github",
    "username": "joedoe",
    "useremail": main_author["email"],
  }])
  main_vcs = vcss[0]  
  version = all_config.get("version", "0.1.0")
  edition = all_config.get("edition", "2018")
  description = all_config.get("description", f"Crate {name}.")
  license = all_config.get("license", "MIT")
  keywords = all_config.get("keywords", ["crate", name])

  repo = f"https://{main_vcs['type']}.com/{main_vcs['username']}/{name}"
  repository = all_config.get("repository", repo)
  homepage = all_config.get("homepage", f"{repo}#{name}")
  documentation = all_config.get("documentation", f"https://docs.rs/{name}/{version}")
  readme = all_config.get("readme", "ReadMe.md")

  package = {
    "name": name,
    "version": version,
    "authors": [f"{author['name']} <{author['email']}>" for author in authors],
    "edition": edition,
    "keywords": keywords,
    "description": description,
    "license": license,
    "repository": repository,
    "homepage": homepage,
    "documentation": documentation,
    "readme": readme,
  }
  bbin = all_config.get("bin", [{
    "name": "example",
    "path": "src/example.rs"
  }])
  dependencies = all_config.get("dependencies", {"dotenv": "0.15.0", "log": "0.4.11"})
  cargo_toml = {
    "package": package,    
    "dependencies": dependencies,
    "bin": bbin,
    "lib": {"path": "src/lib.rs"}
  }
  print(cargo_toml)  
  dump_toml(f"{root}/Cargo.toml", cargo_toml)
  