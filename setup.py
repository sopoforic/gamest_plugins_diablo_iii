from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="gamest-plugins-diablo-iii",
    description="Report on Diablo III games.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sopoforic/gamest_plugins_diablo_iii',
    author="Tracy Poff",
    author_email="tracy.poff@gmail.com",
    packages=['gamest_plugins.diablo_iii'],
    install_requires=['gamest >=2.0, <3.0', 'requests', 'bs4'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Topic :: Games/Entertainment',
    ],
)
