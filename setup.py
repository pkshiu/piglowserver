from distutils.core import setup

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name='PiGlowServer',
      version='0.5',
      author='PK Shiu',
      author_email='pk@pkshiu.com',
      description='A RESTful API server and a web server to control the PiGlow Raspberry Pi Addon Board',
      long_description='A RESTful API server and a web server to control the PiGlow Raspberry Pi Addon Board',
      license='MIT',
      keywords='Raspberry Pi PiGlow Flask Flask-restful Python RESTful',
      url='http://github.com/pkshiu/piglowserver',
      classifiers=classifiers,
      packages=['piglowserver'],
      package_data={'piglowserver': ['templates/*.html']},
      install_requires=['requests', 'flask', 'flask-restful'],
      scripts=['bin/pg_control', 'bin/pg_rest_server'],
      )
