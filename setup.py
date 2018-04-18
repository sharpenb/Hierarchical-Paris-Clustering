from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='paris',
      version='0.0',
      description='Multi-scale modularity based clustering algorithm',
      long_description=readme(),
      classifiers=['Topic :: System :: Clustering',
                   'Programming Language:: Python:: Implementation'],
      keywords='modularity based multi-scale graph clustering',
      url='https://github.com/Charpenb/paris',
      author='Bertrand Charpentier',
      author_email='bercha@kth.se',
      license='MIT',
      packages=['paris'],
      install_requires=['numpy', 'networkx'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

