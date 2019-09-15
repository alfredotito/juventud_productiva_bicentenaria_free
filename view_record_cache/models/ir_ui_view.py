# -*- coding: utf-8 -*-

import hashlib

from openerp import models, fields, api, tools, _,SUPERUSER_ID
from openerp.http import request
from openerp.exceptions import AccessError, MissingError, ValidationError
import logging

_logCache = logging.getLogger(__name__+'_Cache')

PREFETCH_MAX=models.PREFETCH_MAX

class View(models.Model):
    _inherit='ir.ui.view'
    
    #~ @api.model
    #~ @api.returns('self',
        #~ upgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else self.browse(value),
        #~ downgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else value.ids)
    #~ def search(self, args, offset=0, limit=None, order=None, count=False,_cache={}):
    @api.returns('self')
    def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False,_cache={}):
            res=[]
            resUsers=self.pool['res.users']
            groups_id=resUsers.browse(cr,SUPERUSER_ID,[user]).groups_id.ids
            key=str(offset)+str(args)+str(limit or 'limit')+str(order or 'order')+str(count or 'count')+str(groups_id)
            key_hash=str(hashlib.sha1(key or '').hexdigest())
            if not _cache.has_key(key_hash):
                """ search(args[, offset=0][, limit=None][, order=None][, count=False])

                Searches for records based on the ``args``
                :ref:`search domain <reference/orm/domains>`.

                :param args: :ref:`A search domain <reference/orm/domains>`. Use an empty
                             list to match all records.
                :param int offset: number of results to ignore (default: none)
                :param int limit: maximum number of records to return (default: all)
                :param str order: sort string
                :param bool count: if True, only counts and returns the number of matching records (default: False)
                :returns: at most ``limit`` records matching the search criteria

                :raise AccessError: * if user tries to bypass access rules for read on the requested object.
                """
                res = self._search(cr, user, args, offset=offset, limit=limit, order=order, context=context, count=count)
                _cache[key_hash]=res
                _logCache.info('SET ir.ui.view search %s - %d ' % (key_hash, len(_cache)))
            return _cache[key_hash] 
    
    #~ def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):
        #~ """
        #~ Performs a ``search()`` followed by a ``read()``.

        #~ :param cr: database cursor
        #~ :param user: current user id
        #~ :param domain: Search domain, see ``args`` parameter in ``search()``. Defaults to an empty domain that will match all records.
        #~ :param fields: List of fields to read, see ``fields`` parameter in ``read()``. Defaults to all fields.
        #~ :param offset: Number of records to skip, see ``offset`` parameter in ``search()``. Defaults to 0.
        #~ :param limit: Maximum number of records to return, see ``limit`` parameter in ``search()``. Defaults to no limit.
        #~ :param order: Columns to sort result, see ``order`` parameter in ``search()``. Defaults to no sort.
        #~ :param context: context arguments.
        #~ :return: List of dictionaries containing the asked fields.
        #~ :rtype: List of dictionaries.

        #~ """
        #~ groups_id=self.env.user.groups_id.ids
        #~ key=str(domain)+str(fields or 'fields')+str(offset or 'offset')+str(limit or 'limit')+str(order or 'order')+str(groups_id)
        #~ key_hash=str(hashlib.sha1(key or '').hexdigest())
        #~ if not _cache.has_key(key_hash):
            #~ record_ids = self.search(cr, uid, domain or [], offset=offset, limit=limit, order=order, context=context)
            #~ if not record_ids:
                #~ if not self.context.get('install_mode') and self.context.get('website_id'):
                    #~ _cache[key_hash]=[]
                #~ return []
                
            #~ if fields and fields == ['id']:
                #~ # shortcut read if we only want the ids
                #~ if not self.context.get('install_mode') and self.context.get('website_id'):
                    #~ _cache[key_hash]=[{'id': id} for id in record_ids]
                #~ return [{'id': id} for id in record_ids]

            #~ # read() ignores active_test, but it would forward it to any downstream search call
            #~ # (e.g. for x2m or function fields), and this is not the desired behavior, the flag
            #~ # was presumably only meant for the main search().
            #~ # TODO: Move this to read() directly?                                                                                                
            #~ read_ctx = dict(context or {})                                                                                                       
            #~ read_ctx.pop('active_test', None)                                                                                                    
                                                                                                                                                 
            #~ result = self.read(cr, uid, record_ids, fields, context=read_ctx) 
            #~ if len(result) <= 1:
                #~ if not self.context.get('install_mode') and self.context.get('website_id'):
                    #~ _cache[key_hash]=result
                #~ return result

            #~ # reorder read
            #~ index = dict((r['id'], r) for r in result)
            #~ _logCache.info('SET ir.ui.view search_read %s - %d ' % (key_hash, len(_cache)))
            #~ if not self.context.get('install_mode') and self.context.get('website_id'):
                #~ _cache[key_hash]=[index[x] for x in record_ids if x in index]
        #~ if not self.env.context.get('install_mode') and self.env.context.get('website_id'):
           #~ return _cache[key_hash]
        #~ return [index[x] for x in record_ids if x in index]

    
    @api.multi
    @api.v8
    def read(self, fields=None, load='_classic_read',_cache={}):
        """ read([fields])

        Reads the requested fields for the records in ``self``, low-level/RPC
        method. In Python code, prefer :meth:`~.browse`.

        :param fields: list of field names to return (default is all fields)
        :return: a list of dictionaries mapping field names to their values,
                 with one dictionary per record
        :raise AccessError: if user has no read rights on some of the given
                records
        """
        resUsers=self.env['res.users']
        groups_id=resUsers.browse(self.env.uid).groups_id.ids
        key=str(self.ids)+str(fields or 'fields')+str(load)+str(groups_id)
        key_hash=str(hashlib.sha1(key or '').hexdigest())
        if not _cache.has_key(key_hash) or self.env.context.get('install_mode'):
            # check access rights
            self.check_access_rights('read')
            fields = self.check_field_access_rights('read', fields)

            # split fields into stored and computed fields
            stored, computed = [], []
            for name in fields:
                if name in self._columns:
                    stored.append(name)
                elif name in self._fields:
                    computed.append(name)
                else:
                    _logger.warning("%s.read() with unknown field '%s'", self._name, name)

            # fetch stored fields from the database to the cache
            self._read_from_database(stored)

            # retrieve results from records; this takes values from the cache and
            # computes remaining fields
            result = []
            name_fields = [(name, self._fields[name]) for name in (stored + computed)]
            use_name_get = (load == '_classic_read')
            for record in self:
                try:
                    values = {'id': record.id}
                    for name, field in name_fields:
                        values[name] = field.convert_to_read(record[name], use_name_get)
                    result.append(values)
                except MissingError:
                    pass
            if not self.env.context.get('install_mode'):
                    _logCache.info('SET ir.ui.view read %s - %d ' % (key_hash, len(_cache)))
                    _cache[key_hash]=result
        if not self.env.context.get('install_mode') and _cache.has_key(key_hash):
            # store result in cache for POST fields
            result=_cache[key_hash]
            for vals in result:
                record = self.browse([vals['id']])
                record._cache.update(record._convert_to_cache(vals, validate=False))
            return result

        return result
