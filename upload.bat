SET "MYPYTHONPATH=D:\Python37_64" 
set PATH=%MYPYTHONPATH%;%MYPYTHONPATH%\Scripts;C:\Windows\System32

python setup.py sdist bdist_wheel
python -m twine upload --skip-existing dist/*

