.. _cmdusage:

***********************
Commandline Usage
***********************

``Connectome Mapper 3 (CMP3)`` is distributed as a BIDS App which adopts the :abbr:`BIDS (Brain Imaging Data Structure)` standard for data organization and takes as principal input the path of the dataset that is to be processed. The input dataset is required to be in valid `BIDS` format, and it must include at least a T1w or MPRAGE structural image and a DWI and/or resting-state fMRI image. See :ref:`cmpbids` page that provides links for more information about BIDS and BIDS-Apps as well as an example for dataset organization and naming.

.. warning::
    As of ``CMP3 v3.0.0-RC2``, the BIDS App includes a **tracking** system that anonymously reports the run of the BIDS App. This feature has been introduced to support us in the task of fund finding for the development of CMP3 in the future. However, users are still free to opt-out using the ``--notrack`` commandline argument.

.. important:: Since ``v3.0.0-RC4``, configuration files adopt the `JSON` format. If you have your configuration files still in the *old* `INI` format,
    do not worry, the CMP3 BIDS App will convert them to the new `JSON` format automatically for you.

Commandline Arguments
=============================

The command to run ``CMP3`` follows the `BIDS-Apps <https://github.com/BIDS-Apps>`_ definition standard with additional options for loading pipeline configuration files.

.. argparse::
		:ref: cmp.parser.get
		:prog: connectomemapper3

.. important::
    Before using any BIDS App, we highly recommend you to validate your BIDS structured dataset with the free, online `BIDS Validator <http://bids-standard.github.io/bids-validator/>`_.

Participant Level Analysis
===========================
To run the docker image in participant level mode (for one participant):

  .. parsed-literal::

    $ docker run -t --rm -u $(id -u):$(id -g) \\
            -v /home/localadmin/data/ds001:/bids_dir \\
            -v /media/localadmin/data/ds001/derivatives:/output_dir \\
            (-v /usr/local/freesurfer/license.txt:/bids_dir/code/license.txt \\)
            sebastientourbier/connectomemapper-bidsapp:|release| \\
            /bids_dir /output_dir participant --participant_label 01 \\(--session_label 01 \\)
            (--anat_pipeline_config /bids_dir/code/ref_anatomical_config.json \\)
            (--dwi_pipeline_config /bids_dir/code/ref_diffusion_config.json \\)
            (--func_pipeline_config /bids_dir/code/ref_fMRI_config.json \\)
            (--number_of_participants_processed_in_parallel 1)

.. note:: The local directory of the input BIDS dataset (here: ``/home/localadmin/data/ds001``) and the output directory (here: ``/media/localadmin/data/ds001/derivatives``) used to process have to be mapped to the folders ``/bids_dir`` and ``/output_dir`` respectively using the ``-v`` docker run option.

.. important:: The user is requested to use its own Freesurfer license (`available here <https://surfer.nmr.mgh.harvard.edu/registration.html>`_). CMP expects by default to find a copy of the FreeSurfer ``license.txt`` in the ``code/`` folder of the BIDS directory. However, one can also mount with the ``-v`` docker run option a freesurfer ``license.txt``, which can be located anywhere on its computer (as in the example above, i.e. ``/usr/local/freesurfer/license.txt``) to the ``code/`` folder of the BIDS directory inside the docker container (i.e. ``/bids_dir/code/license.txt``).

.. note:: At least a configuration file describing the processing stages of the anatomical pipeline should be provided. Diffusion and/or Functional MRI pipeline are performed only if a configuration file is set. The generation of such configuration files, the execution of the BIDS App docker image and output inpection are facilitated through the use of the Connectome Mapper GUI, i.e. cmpbidsappmanager (see `dedicated documentation page <bidsappmanager.html>`_)

Debugging
=========

Logs are outputted into
``<output dir>/cmp/sub-<participant_label>/sub-<participant_label>_log-cmpbidsapp.txt``.

Support, bugs and new feature requests
=======================================

If you need any support or have any questions, you can post to the `CMTK-users group <http://groups.google.com/group/cmtk-users>`_.

All bugs, concerns and enhancement requests for this software are managed on GitHub and can be submitted at `https://github.com/connectomicslab/connectomemapper3/issues <https://github.com/connectomicslab/connectomemapper3/issues>`_.


Not running on a local machine?
================================

If you intend to run ``CMP3`` on a remote system such as a high-performance computing cluster where Docker is not available due to root privileges, a Singularity image is also built for your convenience and available on `Sylabs.io <https://sylabs.io/>`_. Please see instructions at :ref:`Running on a cluster (HPC) <run-on-hpc>`.

Also, you will need to make your data available within that system first. Comprehensive solutions such as `Datalad <http://www.datalad.org/>`_ will handle data transfers with the appropriate settings and commands. Datalad also performs version control over your data. A tutorial is provided in :ref:`Adopting Datalad for collaboration <datalad-cmp>`.
