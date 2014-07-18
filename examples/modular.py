#!/usr/bin/env python
# coding=utf-8
"""
This is a very basic example of how to use sacred.
"""
from __future__ import division, print_function, unicode_literals
from sacred.experiment import Experiment, Module

# ============== Module 0: settings =================
s = Module("settings")


@s.config
def cfg():
    verbose = True



# ============== Module 1: dataset.paths =================
data_paths = Module("dataset.paths", modules=[s])


@data_paths.config
def cfg(settings):
    v = not settings['verbose']
    base = '/home/sacred/'


# ============== Module 2: dataset =======================
data = Module("dataset", modules=[data_paths, s])


@data.config
def cfg(paths):
    basepath = paths['base'] + 'datasets/'
    filename = "foo.hdf5"


@data.capture
def foo(basepath, filename, paths, settings):
    print(paths)
    print(settings)
    return basepath + filename


# ============== Experiment ==============================
ex = Experiment('modular_example', modules=[data, data_paths])


@ex.config
def cfg(seed, dataset):
    s = seed*2
    a = 10
    b = 17
    c = a + b
    out_base = dataset['paths']['base'] + 'outputs/'
    out_filename = dataset['filename'].replace('.hdf5', '.out')


@ex.automain
def main(a, b, c, out_base, out_filename, dataset):
    print('a =', a)
    print('b =', b)
    print('c =', c)
    print('out_base =', out_base, out_filename)
    # print("dataset", dataset)
    # print("dataset.paths", dataset['paths'])
    print("foo()", foo())
