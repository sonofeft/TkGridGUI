setlocal

SET "MYPYTHONPATH=C:\Python310" 
set PATH=%MYPYTHONPATH%;%MYPYTHONPATH%\Scripts;C:\Windows\System32

python setup.py sdist bdist_wheel
:: python -m twine upload --skip-existing dist/*
C:\Python310\Scripts\twine.exe upload --config-file "%HOMEPATh%\.pypirc" --skip-existing dist/*.*

endlocal
