@echo off
setlocal

set "root=%~dp0..\"
for %%d in (server database controller) do (
    if exist "%root%%%d\requirements.txt" (
        echo Installing packages for %root%%%d\requirements.txt...
        pip install -r "%root%%%d\requirements.txt"
    ) else (
        echo %root%%%d\requirements.txt not found.
    )
)

echo All packages installed.
