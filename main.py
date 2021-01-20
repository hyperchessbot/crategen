import toml
import glob
import os
import json
import subprocess
from shutil import copyfile
import datetime
import string

def create_dirs(path):
  try:
    os.makedirs(path)
  except OSError:
      # print(f"failed to create {path}")
      pass
  else:
      # print(f"created {path}")
      pass

def dump_toml(path, obj):
  with open(path, 'w') as f:
    toml.dump(obj, f)

def dump_json(path, obj):
  with open(path, 'w') as f:
    json.dump(obj, f, indent=2)

def dump_text(path, text):
  with open(path, 'w') as f:
    f.write(text)

def read_text(path):
  with open(path) as f:
    return f.read()

create_dirs("generated")

global_config = toml.load("global.toml")

for filepath in glob.iglob('crates/*.toml'):  
  crate_config = toml.load(filepath)  
  all_config = {**global_config, **crate_config}  
  name = filepath.split("/")[1].split(".toml")[0]
  print("generating", name)
  root = f"generated/{name}"  
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
  bbin = all_config.get("bin", [{"name": "usage"}, {"name": "advanced"}])  
  for cbin in bbin:
    cbin["title"] = cbin.get("title", string.capwords(cbin['name']))
    cbin["path"] = cbin.get("path", f"src/{cbin['name']}.rs")  
  dependencies = all_config.get("dependencies", {"dotenv": "0.15.0", "log": "0.4.11", "env_logger": "0.8.2"})
  package["default-run"] = bbin[0]["name"]
  cargo_toml = {
    "package": package,    
    "dependencies": dependencies,
    "bin": [{"name": cbin["name"], "path": cbin["path"]} for cbin in bbin],
    "lib": {"path": "src/lib.rs"}
  }  
  dump_toml(f"{root}/Cargo.toml", cargo_toml)
  src_root = f"{root}/src"
  create_dirs(src_root)  
  dump_text(f"{src_root}/lib.rs", f"\n// lib\n\npub mod {name};\n")
  dump_text(f"{src_root}/{name}.rs", f"#[derive(Debug)]\npub struct Foo{{}}")
  for cbin in bbin:
    bin_name = cbin["name"]
    dump_text(f"{src_root}/{bin_name}.rs", f'use {name}::{name}::*;\n\nfn main(){{\n\tprintln!("{bin_name} {{:?}}", Foo{{}});\n}}\n')
  p = subprocess.Popen(["git", "init"], cwd=root)
  p.wait()  
  config = """[core]
  repositoryformatversion = 0
  filemode = true
  bare = false
  logallrefupdates = true

"""
  for vcs in vcss:
    vcs_type = vcs["type"]
    username = vcs["username"]
    config += f'[remote "{vcs_type}"]\n'
    config += f'\turl = ' + f"https://{vcs_type}.com/{username}/{name}.git\n"
    config += f'\tfetch = +refs/heads/*:refs/remotes/{vcs_type}/*\n\n'  
  script_root = f"{root}/s"
  create_dirs(script_root)  
  dump_text(f"{script_root}/config", config)  
  
  p = f"""
git config --global user.email "{main_vcs['useremail']}"
git config --global user.name "{main_vcs['username']}"

git checkout -b master

git add . -A

git commit -m "$*"

"""
  for vcs in vcss:
    p = p + f"git push {vcs['type']} master\n\n"
  p = "python s/gen.py\n\n" + p
  dump_text(f"{script_root}/p", p)
  dump_text(f"{script_root}/p.bat", p)
  p = subprocess.Popen(["chmod", "+x", f"p"], cwd=script_root)
  p.wait()  
  copyfile(f"licenses/{license}", f"{root}/LICENSE")
  if license == "MIT":
    mit = read_text("licenses/MIT")
    cr = " , ".join([f"@{author['name']}" for author in authors])
    mit = f"Copyright {datetime.datetime.now().year} {cr}\n" + mit
    dump_text(f"{root}/LICENSE", mit)
  badges = f"[![documentation](https://docs.rs/{name}/badge.svg)](https://docs.rs/{name}) [![Crates.io](https://img.shields.io/crates/v/{name}.svg)](https://crates.io/crates/{name}) [![Crates.io (recent)](https://img.shields.io/crates/dr/{name})](https://crates.io/crates/{name})\n\n"
  readmemd = badges + f"# {name}\n\n{description}"  
  dump_text(f"{root}/ReadMe.md", readmemd)
  dump_text(f"{script_root}/ReadMe.md", readmemd)
  cargo_toml["bin"] = bbin
  conf_json = json.dumps(cargo_toml, indent=2)
  dump_text(f"{script_root}/gen.py", f"config = {conf_json}\n\n" + read_text("gen.py"))
  copyfile(f".gitignore", f"{root}/.gitignore")
  print("done", name)