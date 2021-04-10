#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import numpy as np
from astropy.table import Table
from flows import api, load_config
import seaborn as sns
import matplotlib.pyplot as plt
# Change to directory, raise if it does not exist
config = load_config()
workdir_root = config.get('photometry', 'output', fallback='.')

fids = glob.glob(workdir_root+'/*/*')
fn = '/photometry.ecsv'

zp_errors = []
bad_phots = []
for fi in fids:
    try:
        AT = Table.read(fi+fn)
        if AT.meta['photfilter'] in ['H','J','K']:
            zp_errors.append(min(AT.meta['zp_error'],AT.meta['zp_error_weights']))
    except:
        finame = fi.split('/')[-1]
        bad_phots.append(finame)
        print('fileid {} in SN = {} could not be read, check the photometry'.format(finame,snname))

zp_errors = np.array(zp_errors)
bad_phots = np.array(bad_phots)

with open('zp_errors.npy','w') as f:
    np.save(f,zp_errors)
with open('bad_phots.npy','w') as f:
    np.save(f,bad_phots)

fig, ax = plt.subplots()
g = sns.distplot(zp_errors,ax=ax)
plt.show(block=True)
fig.savefig('zp_errors.png',format='png')
