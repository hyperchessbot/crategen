[![documentation](https://docs.rs/example/badge.svg)](https://docs.rs/example) [![Crates.io](https://img.shields.io/crates/v/example.svg)](https://crates.io/crates/example) [![Crates.io (recent)](https://img.shields.io/crates/dr/example)](https://crates.io/crates/example)

# example

Crate example.

# Usage

```rust
use example::example::*;

fn main(){
	println!("usage {:?}", Foo{});
}
```

# Advanced

```rust
use example::example::*;

fn main(){
	println!("advanced {:?}", Foo{});
}
```

# Logging

```bash
export RUST_LOG=info
# or
export RUST_LOG=debug
```