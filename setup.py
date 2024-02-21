from setuptools import setup, find_packages


setup(
      name='task-manager',
      version='1.0',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      description='It`s a personal helper, witch can be use like the address book, notes manager and file sorter.',
      url='',
      author='',
      author_email='occultnerg@gmail.com',
      license='MIT',
      install_requires=[
            'tabulate==0.9.0',
      ],
      entry_points='''
            [console_scripts]
            manager=bot:run
      ''',
)
