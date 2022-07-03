from setuptools import find_packages, setup

with open("README.rst", "r") as f:
    long_description = f.read()


setup(
    name="disquip-bot",
    version="1.1.8",
    url="https://github.com/blthayer/disquip-bot",
    license="MIT",
    author="Brandon Thayer",
    author_email="brandon.lewis.thayer@gmail.com",
    description="An easy-to-use Discord soundboard bot. BYO audio files "
    "and quip away!",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=find_packages(
        ".", exclude=["tests", "*.tests", "*.tests.*", "service"]
    ),
    install_requires=[
        "attrs==21.4.0",
        "discord.py[voice]==1.7.3",
        "ffmpeg-normalize==1.23.0",
        "tabulate==0.8.10",
    ],
    python_requires=">=3.6",
    setup_requires=["wheel"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": "disquip-bot = disquip:main"},
)
