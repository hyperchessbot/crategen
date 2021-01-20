config = {
  "package": {
    "name": "example",
    "version": "0.1.0",
    "authors": [
      "hyperchessbot <hyperchessbot@gmail.com>"
    ],
    "edition": "2018",
    "keywords": [
      "crate",
      "example"
    ],
    "description": "Crate example.",
    "license": "MIT",
    "repository": "https://github.com/hyperchessbot/example",
    "homepage": "https://github.com/hyperchessbot/example#example",
    "documentation": "https://docs.rs/example/0.1.0",
    "readme": "ReadMe.md",
    "default-run": "usage"
  },
  "dependencies": {
    "dotenv": "0.15.0",
    "log": "0.4.11",
    "env_logger": "0.8.2"
  },
  "bin": [
    {
      "name": "usage",
      "title": "Usage",
      "path": "src/usage.rs"
    },
    {
      "name": "advanced",
      "title": "Advanced",
      "path": "src/advanced.rs"
    }
  ],
  "lib": {
    "path": "src/lib.rs"
  }
}

def dump_text(path, text):
  with open(path, 'w') as f:
    f.write(text)

def read_text(path):
  with open(path) as f:
    return f.read()

def decorate(text, prefix):
  return "\n".join([f"{prefix}{line}" for line in text.split("\n")])

docexamples = []
mdexamples = []
for cbin in config["bin"]:  
  code = read_text(cbin["path"])
  docexamples.append(f"//!\n//! ## {cbin['title']}\n//!\n//!```\n" + decorate(code, "//!") + "```\n//!\n") 
  mdexamples.append(f"# {cbin['title']}\n\n```rust\n" + code + "```\n") 
docexamples = "//!\n//!\n//! # Examples\n//!\n" + "".join(docexamples)
mdexamples = "\n".join(mdexamples)
lib = read_text("src/lib.rs").split("// lib")
lib = docexamples + "\n\n// lib" + lib[1]
dump_text("src/lib.rs", lib)
readme = read_text("s/ReadMe.md")
readme = readme + "\n\n" + mdexamples + """\n# Logging

```bash
export RUST_LOG=info
# or
export RUST_LOG=debug
```"""
dump_text("ReadMe.md", readme)

gitconfig = read_text("s/config")
dump_text(".git/config", gitconfig)
