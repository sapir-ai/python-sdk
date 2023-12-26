from setuptools import setup, find_packages

setup(
    name='sapirai',
    version='0.1.0',
    author='Yu Nakai',
    author_email='y.nakai928@gmail.com',
    description='SDK for sapir.ai',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sapir-ai/python-sdk',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
