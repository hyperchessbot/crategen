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
    "readme": "ReadMe.md"
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

print(config)