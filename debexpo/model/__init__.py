# -*- coding: utf-8 -*-
#
#   __init__.py — Model initialisation code
#
#   This file is part of debexpo - http://debexpo.workaround.org
#
#   Copyright © 2008 Jonny Lamb <jonny@debian.org>
#
#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation
#   files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use,
#   copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following
#   conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#   HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#   OTHER DEALINGS IN THE SOFTWARE.

"""
Model initialization functions.
"""

__author__ = 'Jonny Lamb'
__copyright__ = 'Copyright © 2008 Jonny Lamb'
__license__ = 'MIT'

import sqlalchemy as sa
from sqlalchemy import orm

from debexpo.model import meta

def init_model(engine):
    """
    Initializes the model.
    This should be called before using any of the tables or classes in the model.

    ``engine``
        SQLAlchemy engine to bind to.
    """

    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.session = orm.scoped_session(sm)

def import_all_models():
    """
    Import all models from debexpo.models. This is useful when creating tables.
    """

    from debexpo.model import binary_packages, package_files, packages, source_packages, \
        user_metrics, package_comments, package_info, package_versions, user_countries, \
        users, package_subscriptions

class OrmObject(object):
    """
    A base class for ORM mapped objects.

    This class was found and then altered for debexpo from
    http://www.sqlalchemy.org/trac/wiki/UsageRecipes/GenericOrmBaseClass

    Contributed by ltbarcly (Justin Van Winkle).
    """
    def __init__(self, **kw):
        if not hasattr(self, 'foreign'):
            self.foreign = []

        self.__items__ = []
        for item in dir(self):
            if not item.startswith('_') and item is not "foreign":
                self.__items__.append(item)

        for key in kw:
            if key in self.__items__ or key in self.foreign:
                setattr(self, key, kw[key])
            else:
                raise AttributeError('Cannot set attribute which is ' +
                                     'not column in mapped table: %s' % (key,))

    def __repr__(self):
        atts = []
        for key in self.__items__:
            atts.append((key, getattr(self, key)))

        return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' + repr(x[1]) for x in atts) + ')'

