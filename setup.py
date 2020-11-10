from setuptools import setup, find_packages


setup(
    name='seelab',
    version='1.0.0',
    install_requires=['click'],
    author='Kyungsu',
    author_email='unerue@me.com',
    description='Hi',
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        seelab=seelab.main:main
    """,
)