:: Convenience helper for releasing. Make sure to activate the virtual
:: environment before running.
SET EXITCODE=0

:: Delete old releases. Keep it simple, just delete the directory.
@RD /S /Q dist

:: Build.
python setup.py sdist bdist_wheel
if ERRORLEVEL 1 goto Failed

:: Check.
twine check dist/*
if ERRORLEVEL 1 goto Failed

:: Upload.
python -m twine upload dist/*
if ERRORLEVEL 1 goto Failed

:: End of script.
goto Success

:: Functions for success or failure.
:: https://stackoverflow.com/q/30192627/11052174
:Failed
set EXITCODE=1
:Success
EXIT /B %EXITCODE%