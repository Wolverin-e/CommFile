from setuptools import setup, find_packages
import pathlib

def get_readme() -> str:
    current_dir = pathlib.Path(__file__).parent.resolve()
    readme_path = current_dir/"README.md"
    return readme_path.read_text('utf-8')

setup(
    name='CommFile',
    version='0.0.1',
    description='Executable of MailFile',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author='Mitul Patel',
    author_email='patel.6@iitj.ac.in',
    keywords='communication, mail',
    packages=find_packages(
        include=('MailFile*', )
    ),
    python_requires='>=3.3, <4',
    entry_points={
        'console_scripts': [
            'mm=MailFile.main:main',
        ],
    },
    install_requires=[
        "fusepy",
    ],
    extras_require={
        'dev': [
            'flake8',
            'autopep8'
        ],
    }
)
