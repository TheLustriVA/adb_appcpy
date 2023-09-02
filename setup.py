from setuptools import setup, find_packages

setup(
    name='adb_appcpy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Pillow',
        'pytesseract'
    ],
    entry_points='''
        [console_scripts]
        adb_appcpy=adb_appcpy.cli:cli
    ''',
)
