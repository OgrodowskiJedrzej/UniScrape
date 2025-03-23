import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        os.makedirs('to_scrape/pdfs', exist_ok=True)
        with open('to_scrape/urls_to_scrape.csv', 'w') as f:
            f.write('url\n')
        install.run(self)


setup(
    name='UniScrape',
    packages=['uniscrape'],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
