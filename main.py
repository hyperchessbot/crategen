import toml
import glob

global_config = toml.load("global.toml")

print(global_config)

for filepath in glob.iglob('crates/*.toml'):
    print(filepath)
    crate_config = toml.load(filepath)
    print(crate_config)
    all_config = {**global_config, **crate_config}
    print(all_config)
