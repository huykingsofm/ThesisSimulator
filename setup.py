import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description += "\n"


with open("CHANGELOG.md", "r", encoding="utf-8") as fh:
    long_description += fh.read()


setuptools.setup(
    name="simulator",
    version="0.0.1",
    author="huykingsofm",
    author_email="huykingsofm@gmail.com",
    description="The simulator of my thesis at UIT - 2021",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7.1",
    install_requires=["csbuilder>=0.0.2", "sft>=0.0.2", "hks_pylib>=0.0.8"]
)