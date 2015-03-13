from setuptools import setup, find_packages

setup(
    name='raceresults',
    version='0.0.0',
    author='John Evans',
    author_email='john.g.evans.ne@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['activerr = rr.command_line:run_active',
                            'brrr = rr.command_line:run_bestrace',
                            'crrr = rr.command_line:run_coolrunning',
                            'csrr = rr.command_line:run_compuscore',
                            'nyrr = rr.command_line:run_nyrr']},
    description='Race results parsing',
    install_requires=['lxml>=2.3.4',
                      'requests>=2.2.0',
                      'cssselect>=0.9.1',
                      'pandas>=0.15.2'],
    classifiers=["Programming Language :: Python",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "License :: OSI Approved :: MIT License",
                 "Development Status :: 4 - Beta",
                 "Operating System :: MacOS",
                 "Operating System :: POSIX :: Linux",
                 "Intended Audience :: Developers",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Text Processing :: Markup :: HTML",
                 ]
)