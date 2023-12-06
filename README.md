# [latest.cat](https://latest.cat)

## Shell usage examples

```bash
curl -Lfs latest.cat/php

# you can filter versions
curl -Lfs latest.cat/python@3.17

pyenv install $(curl -Lfs latest.cat/python@3.11)
```
