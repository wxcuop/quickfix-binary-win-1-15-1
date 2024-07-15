import glob
import sys
import sysconfig
from distutils.command.build_ext import build_ext
from setuptools import setup, Extension
from datetime import datetime, timezone

class build_ext_subclass(build_ext):
    def build_extensions(self):
        self.compiler.define_macro("PYTHON_MAJOR_VERSION", sys.version_info[0])
        build_ext.build_extensions(self)

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
cfg_vars = sysconfig.get_config_vars()
for key, value in cfg_vars.items():
    if isinstance(value, str):
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

# Get the current UTC date
utc_now = datetime.now(timezone.utc).strftime('%Y%m%d')

long_description = ''
with open('LICENSE') as file:
    license_ = file.read()

setup(
    name='quickfix-binary',
    version='1.15.1',
    py_modules=[
        'quickfix', 'quickfixt11', 'quickfix40', 'quickfix41', 'quickfix42',
        'quickfix43', 'quickfix44', 'quickfix50', 'quickfix50sp1', 'quickfix50sp2'
    ],
    data_files=[('share/quickfix', glob.glob('spec/FIX*.xml'))],
    author='Oren Miller',
    author_email='oren@quickfixengine.org',
    maintainer='wxcuop',
    description="FIX (Financial Information eXchange) protocol implementation",
    url='http://www.quickfixengine.org',
    download_url='http://www.quickfixengine.org',
    include_dirs=['C++', 'C:/Program Files/OpenSSL-Win64/include'],  # Default path for OpenSSL include directory
    libraries=[
        ('ssl', {
            'include_dirs': ['C:/Program Files/OpenSSL-Win64/include'],
            'library_dirs': ['C:/Program Files/OpenSSL-Win64/lib'],
            'libraries': ['ssl']
        }),
        ('crypto', {
            'include_dirs': ['C:/Program Files/OpenSSL-Win64/include'],
            'library_dirs': ['C:/Program Files/OpenSSL-Win64/lib'],
            'libraries': ['crypto']
        })
    ],
    license=license_,
    cmdclass={'build_ext': build_ext_subclass},
    ext_modules=[Extension(
        '_quickfix', glob.glob('C++/*.cpp'),
        include_dirs=['C++', 'C:/Program Files/OpenSSL-Win64/include'],
        library_dirs=['C:/Program Files/OpenSSL-Win64/lib'],
        libraries=['ssl', 'crypto'],
        extra_link_args=[]
    )]
)
