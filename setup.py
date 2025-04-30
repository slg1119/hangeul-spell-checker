from setuptools import setup, find_packages


def install():
    required = []
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
        for req in requirements:
            p = req.split("==")
            required.append(p[0])
    desc = ""
    setup(
        name="hangeul-spell-checker",
        version="1.1",
        description=desc,
        long_description=desc,
        author="SuHun Han",
        author_email="ssut@ssut.me",
        url="https://github.com/slg1119/hangeul-spell-checker",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "License :: Freeware",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Education",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
        packages=find_packages(),
        install_requires=required,
    )


if __name__ == "__main__":
    install()
