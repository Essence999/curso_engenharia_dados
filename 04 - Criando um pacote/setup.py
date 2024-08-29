from setuptools import setup, find_packages

setup(
    name='pacote',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='Pacote para testes de requisição',
    author='Gabriel',
    author_email='gabriel@exemplo.com',
    url='https://github.com/Essence999/curso_engenharia_dados',
)
