# Copyright (C) 2009-2021, Ecole Polytechnique Federale de Lausanne (EPFL) and
# Hospital Center and University of Lausanne (UNIL-CHUV), Switzerland, and CMP3 contributors
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

"""Provides interfaces for functions provided by Camino-Tackvis missing in nipype or modified.

.. note:
    Module not used anymore by CMP3.
"""

import os
from nipype.interfaces.base import CommandLineInputSpec, CommandLine, traits, TraitedSpec, File
from nipype.utils.filemanip import split_filename


class Camino2TrackvisInputSpec(CommandLineInputSpec):
    in_file = File(exists=True, argstr='-i %s', mandatory=True, position=1,
                   desc='The input .Bfloat (camino) file.')

    out_file = File(argstr='-o %s', genfile=True, mandatory=False, position=2,
                    desc='The filename to which to write the .trk (trackvis) file.')

    min_length = traits.Float(argstr='-l %d', mandatory=False, position=3,
                              units='mm', desc='The minimum length of tracts to output')

    data_dims = traits.List(traits.Int, argstr='-d %s', sep=',',
                            mandatory=False, position=4, minlen=3, maxlen=3,
                            desc='Three comma-separated integers giving the number of voxels along each dimension of the source scans.')

    voxel_dims = traits.List(traits.Float, argstr='-x %s', sep=',',
                             mandatory=False, position=5, minlen=3, maxlen=3,
                             desc='Three comma-separated numbers giving the size of each voxel in mm.')

    # Change to enum with all combinations? i.e. LAS, LPI, RAS, etc..
    voxel_order = File(argstr='--voxel-order %s', mandatory=False, position=6,
                       desc='Set the order in which various directions were stored.\
        Specify with three letters consisting of one each  \
        from the pairs LR, AP, and SI. These stand for Left-Right, \
        Anterior-Posterior, and Superior-Inferior.  \
        Whichever is specified in each position will  \
        be the direction of increasing order.  \
        Read coordinate system from a NIfTI file.')

    nifti_file = File(argstr='--nifti %s', exists=True,
                      mandatory=False, position=7, desc='Read coordinate system from a NIfTI file.')

    phys_coords = traits.Bool(argstr='--phys-coords', mandatory=False, position=8,
                              desc='Treat the input tract points as physical coordinates (relevant for the updated camino track command).')


class Camino2TrackvisOutputSpec(TraitedSpec):
    trackvis = File(
        exists=True, desc='The filename to which to write the .trk (trackvis) file.')


class Camino2Trackvis(CommandLine):
    """Wraps camino_to_trackvis from Camino-Trackvis.

    Convert files from camino .Bfloat format to trackvis .trk format.

    Example
    -------
    >>> import cmtklib.interfaces.camino2trackvis as cam2trk
    >>> c2t = cam2trk.Camino2Trackvis()
    >>> c2t.inputs.in_file = 'data.Bfloat'
    >>> c2t.inputs.out_file = 'streamlines.trk'
    >>> c2t.inputs.min_length = 30
    >>> c2t.inputs.data_dims = [128, 104, 64]
    >>> c2t.inputs.voxel_dims = [2.0, 2.0, 2.0]
    >>> c2t.inputs.voxel_order = 'LAS'
    >>> c2t.run()                  # doctest: +SKIP
    """

    _cmd = 'camino_to_trackvis'
    input_spec = Camino2TrackvisInputSpec
    output_spec = Camino2TrackvisOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['trackvis'] = os.path.abspath(self._gen_outfilename())
        return outputs

    def _gen_filename(self, name):
        if name is 'out_file':
            return self._gen_outfilename()
        else:
            return None

    def _gen_outfilename(self):
        _, name, _ = split_filename(self.inputs.in_file)
        return name + '.trk'
