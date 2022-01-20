from setuptools import find_packages, setup


def read(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except IOError:
        return ""


setup(
    name="discord-types",
    version="0.0.1",
    description="Data structures parsed from Discord's API docs",
    long_description=read("README.md"),
    packages=find_packages(),
    install_requires=read("requirements.txt").splitlines(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
