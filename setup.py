from setuptools import setup, find_packages


setup(
    name='seelab',
    version='0.0.1',
    install_requires=['click', 'tqdm', 'Pillow', 'labelme'],
    author='Kyungsu',
    author_email='unerue@me.com',
    description='Hi',
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        seelab=seelab.main:main
    """,
)