from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python_paris',
      version='0.0.1',
      description='Multi-scale modularity based clustering algorithm',
      long_description=readme(),
      classifiers=['Topic :: System :: Clustering'],
      keywords='modularity multi-scale hierarchical graph clustering',
      url='https://github.com/Charpenb/paris',
      author='Bertrand Charpentier',
      author_email='bercha@kth.se',
      license='Apache License 2.0',
      packages=['python_paris'],
      install_requires=['numpy', 'networkx'],
      test_suite='nose.collector',
      tests_require=['nose', 'matplotlib', 'python-louvain'],
      zip_safe=False)
