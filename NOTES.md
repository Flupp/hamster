# Test commands

```
13:37 act@cat, a, b, c, #d, e, #f, g
```


# Execute GUI

```sh
mkdir -p build/data && glib-compile-schemas --targetdir=build/data data && GSETTINGS_SCHEMA_DIR=build/data python3 src/hamster-service.py & GSETTINGS_SCHEMA_DIR=build/data python src/hamster-cli.py; pkill -ef hamster
```


# Execute tests

```sh
clear && mkdir -p build/data && glib-compile-schemas --targetdir=build/data data && GSETTINGS_SCHEMA_DIR=build/data python -m unittest
```
