from setuptools import setup, find_packages

setup(
    name='cube_3d_render',
    version='0.1.0',
    author='Remy-Pa',
    author_email='remy.paquette@gmail.com',
    description='Adds an App class which takes in lists of coordinates and generates a window rendering cubes at the specified coordinates using OpenGL and pygame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Remy-Pa/cube_3d_render/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pygame',
        'PyOpenGL',
        'PyOpenGL-accelerate',
        'numpy'        
    ],
)
