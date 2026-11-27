# References: TROUBLESHOOTING.md

## 1. Kaggle CLI: ModuleNotFoundError: No module named 'six'
- **Cause**: On Python 3.14+, `six` is not bundled by default, but `kaggle` models import `six`.
- **Fix**: Reinstall with `--with six`:
  ```bash
  uv tool install --with six kaggle --force
  ```

## 2. Wrangler: workerd / esbuild spawn error
- **Cause**: Global npm install skipped native postinstall scripts.
- **Fix**: Reinstall with `--allow-scripts`:
  ```bash
  npm install -g --allow-scripts=esbuild,workerd wrangler
  ```

## 3. Command Not Found after Installation
- **Cause**: Current shell session has not reloaded `.bashrc`.
- **Fix**:
  ```bash
  source ~/.bashrc
  ```
