from setuptools import setup

setup(
    name="django-jsonfield-compat",
    version='0.3.0',
    description="Compatability layer between django-jsonfield and Django's native JSONField",
    long_description=open("README.md").read(),
    url="http://github.com/kbussell/django-jsonfield-compat/",
    author="Keith Bussell",
    author_email="kbussell@gmail.com",
    packages=[
        "jsonfield_compat",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    zip_safe=False,
)
