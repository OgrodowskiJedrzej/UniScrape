import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        os.makedirs('to_scrape/pdfs', exist_ok=True)
        with open('to_scrape/urls_to_scrape.csv', 'w') as f:
            f.write('url\n')

        os.makedirs('logs/', exist_ok=True)
        log_file_path = os.path.join('logs/', 'app_log.log')
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w') as f:
                pass

        os.makedirs('visited', exist_ok=True)

        install.run(self)


setup(
    name='UniScrape',
    packages=['uniscrape'],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
