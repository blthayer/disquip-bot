from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='disquip-bot',
    version='0.1.0',
    url='https://github.com/blthayer/disquip-bot',
    license='MIT',
    author='Brandon Thayer',
    author_email='brandon.lewis.thayer@gmail.com',
    description='An easy-to-use Discord soundboard bot. BYO audio files ' 
                'and quip away!',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(".", exclude=['tests', '*.tests', '*.tests.*']),
    install_requires=['attrs', 'discord.py[voice]', 'tabulate'],
    python_requires='>=3.7',
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
    ],
    entry_points={
        'console_scripts': 'disquip-bot = disquip:main'
    }
)
