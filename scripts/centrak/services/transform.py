"""
Transform json data from on form to another.                             
"""


RULES = {
    'instance': {
        'excludes': [
            '_bamboo_dataset_id',
            'meta/instanceID',
            '_geolocation',
        ],
        'name_map': {
            'house_no': 'no',
            'multi_source': 'multi',
            'occupant_status': 'occupant',
            'neighbour_rseqid': 'neighbour_rseq',
            'cust_gps_coord': 'gps',
            'rseqId': 'rseq',
        },
    }
}


def to_nested_dict(d):
    """Unflatten the dictionary keys used in the provided dictionary"""
    target = {}
    rules_excl = RULES['instance']['excludes']
    rules_nmap = RULES['instance']['name_map']

    for k, v in d.items():
        if k in rules_excl:
            continue

        if '/' in k:
            # flatten key
            key, ikey = k.split('/')
            if key.endswith('_info'):
                key = key.replace('_info','')
            
            if ikey in rules_nmap:
                ikey = rules_nmap[ikey]
            
            if '_' in ikey:
                ikey = '_'.join(ikey.split('_')[1:])

            # set keys
            if key not in target:
                target[key] = {}
            target[key][ikey] = v
        else:
            target[k] = v
    
    # direct transform
    #--------------------------------------------------------
    gps = target['address']['gps_coord']
    target['gps_coord'] = [float(v) for v in gps.split(' ')]
    del target['address']['gps_coord']
    
    target['rseq'] = target['source']['rseqId']
    del target['source']['rseqId']
    if 'kg_id' in target['source']:
        target['kangis_id'] = target['source']['kg_id']
    del target['source']

    target['title_holder'] = target['address']['tholder']
    del target['address']['tholder']

    target['enum_id'] = target['enum']['id']
    del target['enum']

    target['meter']['status'] = target['meter_status']
    del target['meter_status']

    # return processed dict
    return target


def to_flatten_dict(entry):
    """Remove group names from key-name"""
    target = {}
    rules_excl = RULES['instance']['excludes']
    rules_nmap = RULES['instance']['name_map']

    for k, v in entry.items():
        if k in rules_excl:
            continue

        if '/'  in k:
            # exclude entries
            key, ikey = k.split('/')
            if ikey in rules_excl:
                continue

            # re-map names
            if ikey in rules_nmap:
                ikey = rules_nmap[ikey]
            
            target[ikey] = v
        else:
            target[k] = v

    # other transforms
    #----------------------------------------------------------
    target['gps'] = [float(v) for v in target['gps'].split(' ')]
    
    # set xform_id
    parts = target['_xform_id_string'].split('_')
    xform_id = '%s_%s_%s' % (parts[0], parts[1][:2],  parts[2])
    target['xform_id'] = xform_id

    return target

