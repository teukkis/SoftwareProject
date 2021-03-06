from setuptools import setup, find_packages

setup(
    name='backend',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        "flask-cors",
        "flask-sqlalchemy",
        "SQLAlchemy",
        "jsonschema",
        "flask-restful",
        "pycryptodome"
    ],
)
