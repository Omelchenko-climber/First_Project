from setuptools import setup, find_packages


setup(
      name='task-manager',
      version='1.0',
      py_modules= ['bot', 'models', 'contact_manager', 'event_manager', 'note_manager', 'file_sorter', 'base_view', 'common'],
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
      packages=find_packages(where='src'),
      package_dir= {'': 'src'}
)
