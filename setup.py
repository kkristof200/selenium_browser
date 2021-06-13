import setuptools, os

readme_path = 'README.md'

if os.path.exists(readme_path):
    with open(readme_path, 'r') as f:
        long_description = f.read()
else:
    long_description = 'selenium_browser'

setuptools.setup(
    name='selenium_browser',
    version='0.0.6',
    author='Kristóf-Attila Kovács',
    description='selenium_browser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kkristof200/selenium_browser',
    packages=setuptools.find_packages(),
    install_requires=[
        'k-selenium-cookies>=0.0.4',
        'kproxy>=0.0.1',
        'noraise>=0.0.16',
        'selenium>=3.141.0',
        'xpath-utils>=0.0.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.4',
)