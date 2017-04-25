#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def jsonify(source_dict):
    return json.dumps(dict([(k, v) for k, v in source_dict.iteritems() if(v) ]), ensure_ascii=False, indent=4, sort_keys=True)