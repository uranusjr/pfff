"""PEP 517 Build backend interface.
"""

import os

import flit.buildapi
import flit.inifile
import requirementslib


def _convert_requirement(r):
    return '{name}{extra}{version}{marker}'.format(
        name=r.req.line_part,
        extra=r.extras_as_pip,
        version=' ({})'.format(r.specifiers) if r.specifiers else '',
        marker=r.markers_as_pip,
    )


def _collect_pipfile_requires():
    packages = {'packages': [], 'dev-packages': []}
    for section in requirementslib.Pipfile.load(os.getcwd()).sections:
        try:
            ls = packages[section.name]
        except KeyError:
            continue
        ls.extend(
            _convert_requirement(r)
            for r in section.requirements
            if r.is_named
        )
    return packages['packages'], packages['dev-packages']


_read_pkg_ini = flit.inifile.read_pkg_ini


def read_pkg_ini(path):
    default, develop = _collect_pipfile_requires()
    result = _read_pkg_ini(path)
    for key, ls in [('requires_dist', default), ('dev_requires', develop)]:
        existing = result['metadata'].get(key, [])
        existing.extend(ls)
        result['metadata'][key] = existing
        result['raw_config']['metadata'][key] = existing
    return result


# Monley-patch Flit to read Pipfile!
flit.inifile.read_pkg_ini = flit.buildapi.read_pkg_ini = read_pkg_ini

# Use Flit's interface.
from flit.buildapi import *     # noqa
