import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


def read_requirements(filename):
    with open(filename, 'r') as file:
        return [line for line in file.readlines() if not line.startswith('-')]


requirements = read_requirements('requirements.txt')

setuptools.setup(
    name="pipe-framework",
    version="0.0.1",
    author="NeZanyat",
    author_email="rlatyshenki@gmail.com",
    description="Data oriented web framework",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="None",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
