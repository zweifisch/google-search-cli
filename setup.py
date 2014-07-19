from setuptools import setup

setup(
    name='google-search-cli',
    version='0.0.5',
    url='https://github.com/zweifisch/google-search-cli',
    license='MIT',
    description='google search cli',
    keywords='google search cli',
    long_description=open('README.md').read(),
    author='Feng Zhou',
    author_email='zf.pascal@gmail.com',
    packages=['google_search_cli'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': ['google-search=google_search_cli:run'],
    },
)
