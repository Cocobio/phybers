"""Segmentation Module
"""

import os
import sys
import numpy as np
from pathlib import Path
from .fiberseg.c_wrappers import segment
from ..utils import sampling, read_bundle, write_bundle


def fiberseg(file_in: str, id_subj: str, atlas_dir: str, atlas_info: str, dir_out: str) -> None:
    """
    White matter fiber bundle segmentation algorithm based on a multi-subject atlas.
    
    Parameters
    ----------
    file_in : str
        Tractography data file in *'.bundles'* format.
    id_subj : str
        Subject identification number, used to label the results.
    atlas_dir : str
        Bundle atlas, with bundles in separated files, sampled at 21 equidistant points. The bundle atlases provided are in same folders.
    atlas_info : str
        Text file that stores information about the brain fiber atlas, such as the fascicle name, segmentation threshold, and fascicle size.
        Note that the segmentation threshold can be adjusted depending on the database to be used.
    dir_out : str
        Directory name to store all the results generated by the algorithm.

    Return
    ------
    None

    Notes
    -----
    This function generates the following files in the specified directory:    
    
    Segmented fibers : bundles files
        Directory contains all atlas fascicles extracted from the subject, saved as separate files in the '.bundles' format. 
        Each file's name is composed of the atlas label followed by the subject's ID
    Centroids : bundles file
        Directory that contains the centroid for each fascicle segmented in same *'.bundles'* files. 
    Index of fibers per fasciculus : text file
        Text file containing the indexes of the fibers that were segmented by each fascicle of the atlas.
        
    Examples
    --------
    To use the `fiberseg()` function, you need to download the tractography data from the `link fiberseg  <https://www.dropbox.com/sh/tj67742sxvmqfg1/AAD_J41rw4E70OVFayAy18T6a?dl=1>`_ .
    Then, you can run the following code in a Python terminal:

    >>> from phybers.segment import fiberseg
    >>> file_in = 'path_to_tractography_data.bundles'
    >>> id_subj = '01'
    >>> atlas_dir = 'path_to_atlas/bundles'
    >>> atlas_info = 'path_to_atlas/atlas_info.txt'
    >>> dir_out = 'path_to_output_directory'
    >>> fiberseg(file_in, id_subj, atlas_dir, atlas_info, dir_out)

    Note: Make sure to replace 'path_to_tractography_data', 'path_to_atlas', and 'path_to_output_directory' with the actual paths to your data and directories. 
    
    """


    id_seg_result= os.path.join(dir_out,'idx_bundles')
    os.makedirs(id_seg_result, exist_ok=True)

    has21points = True
    data=read_bundle(file_in)

    for i in range(len(data)-1):
        if len(data[i]) != len(data[i+1]):
            has21points = False
            break

    final_bundles21p_dir = os.path.join(dir_out, 'FinalBundles21p')
    os.makedirs(final_bundles21p_dir, exist_ok=True)

    if not has21points:

        final_bundles_dir = os.path.join(dir_out, 'FinalBundles')
        os.makedirs(final_bundles_dir, exist_ok=True)

        outfile_dir= os.path.join(dir_out, 'outfile')
        os.makedirs(outfile_dir, exist_ok=True)

        fibers21p = os.path.join(outfile_dir,'fiberorig_21p.bundles')

        sampling(file_in, fibers21p, 21)

        segment(21, fibers21p, id_subj, atlas_dir, atlas_info,
                final_bundles21p_dir, id_seg_result)

        for i in os.listdir(id_seg_result):
            index=[]
            with open (os.path.join(id_seg_result,i)) as file:
                for line in file:
                    index.append(int(float(line.strip())))
            bun = np.array(data, dtype='object')[index]
            write_bundle(os.path.join(final_bundles_dir,id_subj+'_to_'+i[:-4]+'.bundles'), bun)

    else:
        segment(21, file_in, id_subj, atlas_dir, atlas_info,
                final_bundles21p_dir, id_seg_result)
