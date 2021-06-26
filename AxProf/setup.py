import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AxProf",
    version="0.0.1",
    author="Keyur Joshi et al",
    author_email="kpjoshi2@illinois.edu",
    description="AxProf Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://axprof.org/",
    project_urls={
        "Bug Tracker": "https://github.com/uiuc-arc/AxProf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
