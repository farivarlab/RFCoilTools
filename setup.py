from setuptools import setup, find_packages

setup(
    name='RFCoilTools',
    version='0.0.1',
    description='RF Coil Design and Evaluation Tools',
    license='MIT',
    #packages=['RFCoilTools'],
    author='William Mathieu',
    author_email='william.mathieu@mail.mcgill.ca',
    keywords=['RF Coils','MRI'],
    url='https://github.com/WilliamMathieu/RFCoilTools',
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'ipython',
        'jupyter',
        'pandas',
        'sympy',
        'nose',
        'dicom2nifti',
        'nibabel',
        'Pillow',
        'scikit-rf']
)
