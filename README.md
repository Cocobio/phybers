﻿# Phybers Documentation
 > ## _phybers.segment_
 
 > > ### _Description_

This module includes a white matter fiber bundle segmentation algorithm ([Guevara et al., 2012][Pg2012], [Labra et al., 2017][LN2017], [Vazquez et al., 2019][An2019]) based on a multi-subject atlas.  The method uses as a measure of similarity between pairs of fibers the maximum Euclidean distance between corresponding points ($d_{ME}$), defined as:

$$
d_{ME}(A,B) = \min(\max_{i}(|a_{i}-b_{i}|),\max_{i}(|a_{i}-b_{N_{p}-i}|))  \\ \\ \\ \\   [1]
$$

where $a_{i}$ and $b_{i}$ are the 3D coordinates of the points of fibers A and B respectively, in direct order, and $b_{N_{p}-i}$ are the 3D coordinates of the points of fibers B in flipped order. $N_{p}$ is the number of fiber points.

It aims to classify the subject fibers according to a multi-subject bundle atlas. The bundle atlas consists of a set of representative bundles and an information file. The fibers of the atlas bundles are called centroids. The fibers of each subject are classified using a maximum $d_{ME}$ distance threshold for each bundle between the subject’s fibers and the atlas centroids. The fibers are labeled with the closest atlas bundle, given that the distance is smaller than the distance threshold.

We provide one atlas of deep white matter (DWM) bundles ([Guevara et al., 2012][Pg2012]) and one atlas of superficial white matter (SWM) bundles, [Roman et al., 2017][cl2017]. Furthermore, other atlases are available for downloading from the Phybers website, such as a new SWM bundle atlas  ([Roman et al., 2022][cl2022]), and the DWM and SWM bundle atlas of [Zhang et al., 2018][zhang2018] in the format required by the segmentation algorithm. All the atlases are in the MNI space.

> > ### _Functions_

```python
def fiberseg(fiber_input: str, idsubj: str, atlasdir: str, atlasInformation: str, result_path: str) -> None
```

> > ### _Parameters_
The inputs are:

-	 ***fiber_input***: the tractography data file that contains the fibers of the whole brain of a subject. These must be in the same reference system as the used bundle atlas and be in bundles format.
-	 ***idsubj***: the subject identification number, used to label the results
-	 ***atlasdir***: the bundle atlas, with bundles in separated files, sampled at 21 equidistant points. The bundle atlases provided are in different folders.
-	***atlasInformation***: a text file that stores information needed to apply the segmentation algorithm such as the name of the atlas fascicle and the segmentation threshold. Note that the segmentation threshold can be adjusted depending on the database to be used.
-	 ***result_path***: the directory name to store all the results generated by the algorithm.


The outputs files are:

-	***Segmented fibers***_: the atlas fascicles extracted in the subject, which are labeled and saved in bundles format.

-	***Centroids***: the centroid of each segmented fascicle.

-	***Index of fibers per fasciculus***: a text file containing the indexes of the fibers that were segmented by each fascicle of the atlas.


> > ### Example
To test `fiberseg()`, download the data from the link provided [link to be provided][datafiberseg]. Then, open a Python terminal and run the following commands.

```python
from phybers.segment import fiberseg
fiberseg('subject_01.bundles', '01', 'atlas/bundles', 'atlas/atlas_info.txt', 'resultseg')
```
You will locate the segmentation results in the 'resultseg' directory

#
 > ## _phybers.clustering_
 > > ### _Description_
The module comprises two algorithms for clustering cerebral fibers, HClust (Clustering Hierarchical, [Roman et al., 2017][cl2017], [ 2022][cl2022]) y FFClust (Fast Fiber Clustering, [Vázquez et al., 2020][va2020])

 > > ### _phybers.clustering.hclust_
 > > > ### _Description_

HClust is an average-link hierarchical agglomerative clustering algorithm which allows finding bundles based on a pairwise fiber distance measure. The algorithm calculates a distance matrix between all fiber pairs for a bundles dataset ($d_{ij}$), by using the maximum of the Euclidean distance between fiber pairs (Equation [1]). Then, it computes an affinity graph on the $d_{ij}$ matrix for the fiber pairs that have Euclidean distance below a maximum distance threshold ( MaxDistance_Threshold). The Affinity ([Donnell and Westin, 2007][od2007]) is given by the following equation:

$$
a_{ij} = e^{\frac{-d_{ij}}{\sigma^{2}}}  \\ \\ \\ \\   [2]
$$

where $d_{ij}$ is the distance between the elements $i$ and $j$, and $\sigma$ is a parameter that defines the similarity scale in $mm$.

From the affinity graph, the hierarchical tree is generated using an agglomerative average-link hierarchical clustering algorithm. The tree is adaptively partitioned using a distance threshold (***PartDistance_Threshold***). 

> > > ### _HClust Functions_

```python
def hclust(fiber_input: str, PartDistance_Threshold: int,  MaxDistance_Threshold: int, var: int, work_dir: str) -> None
```
> > >### _HClust  Parameters_

The inputs are:
-	***fiber_input***: the tractography data file.
-	***PartDistance_Threshold***: a partition threshold (in $mm$), default $40$ $mm$.
-	***MaxDistance_Threshold***: a maximum distance threshold (in $mm$), default $30$ $mm$.
-	***var***: variance squared and provides a similarity scale (in $mm$), its default value is $3600$ $mm$
-	***work_dir***: the directory to store all the results generated by the algorithm.

The outputs files are:
-	***Clusters***: the directory that stores all the fiber clusters found.
-	***Centroids***: the directory that contains the centroids for each created cluster.
-	***Index of fibers per clusters***: a text file storing the fiber indexes for each of the detected clusters.

> > > ### _HClust Example_
To test `hclust()`,  download the data from the link provided [link to be provided][datahclust]. Then, open a Python terminal and run the following commands.

```python
from phybers.clustering import hclust
hclust (fiber_input='fibers_test.bundles', PartDistance_Threshold=40, MaxDistance_Threshold=30, var =3600, work_dir= 'hclust_result')
```

You will locate the segmentation results in the 'hclust_result' directory

 > > ### _phybers.clustering.ffclust_
 > > > ### _Description_

FFClust is an intra-subject clustering algorithm aims to identify compact and homogeneous fiber clusters on a large tractography dataset.  The algorithm consists of four stages. The stage 1 applies Minibatch K-Means clustering on five fiber points, and it merges fibers sharing the same point clusters (map clustering) in stage 2. Next, it reassigns small clusters to bigger ones (stage 3) considering distance of fibers in direct and reverse order. Finally, at stage 4, the algorithm groups clusters sharing the central point and merges close clusters represented by their centroids. The distance among fibers is defined as the maximum of the Euclidean distance between corresponding points. The algorithm supports sequential and parallel execution using OpenMP.

> > > ### _FFClust Functions_

```python
def ffclust(infile: str, output_directory: str, thr_assign: int = 6, thr_join: int = 6) -> bool
```
> > >### _FFClust  Parameters_

The inputs are:
-	***infile***: the input tractography dataset.
-	***output_directory***: the directory to store all the results generated by the algorithm.
-	***thr_assign***: a maximum distance threshold for the cluster reassignment in mm, default: $6.0$
-	***thr_join***: a maximum distance threshold for the cluster merge in mm, default: $6.0$


The outputs files are:
-	***Clusters***: the final fiber clusters.
-	***Centroids***: the directory that stores the centroids for each created cluster.
-	***Index of fibers per cluster***: the text file storing the fiber indexes for each of the detected clusters.


> > > ### _FFClust Example_
To test `ffclust()`,  download the data from the link provided [link to be provided][dataffclust]. Then, open a Python terminal and run the following commands.

```python
from phybers.clustering import ffclust
ffclust (infile='fibers_test.bundles', output_directory='ffclust_result', thr_assign=6, thr_join=6)
```
You will locate the segmentation results in the 'ffclust_result' directory

# 
 > ## _phybers.utils_
 > > ### _Description_
The ***utils*** are a set of tools used for tractography preprocessing and the analysis of brain fiber clustering and segmentation results. The module includes tools for reading and writing brain fiber files in bundles format, transform the fibers to a reference coordinate system based on a deformation field, sampling of fibers at n equidistant points, calculation of intersection between sets of brain fibers, and tools for extracting measures and filtering fiber clusters or segmented bundles. We considered the extraction of measures such as size, length and the distance between fibers of each cluster (or fascicle)

 > > ### _phybers.utils.deform_
 > > > ### _Description_

The ***deformation*** sub-module transforms a tractography file to another space using a non-linear deformation file. The maps must be stored in NIfTI format, where the voxels contain the transformation to be applied to each voxel 3D space location. The Deform sub-module applies the deformation to the 3D coordinates of the fiber points. 

> > > ### _deform Functions_

```python
def deform(imgdef: str, infile: str, outfile: str) -> None
```
> > >### _deform  Parameters_

The inputs are:
-	***imgdef***: deformation image (image in NIfTI format containing the deformations)
-	***infile***: input tractography dataset
-	***outfile***: path to the transformed tractography dataset

The outputs files are:
-	 tractography dataset that has been transformed into the MNI space.

> > > ### _deform Example_
To test `deform()`,  download the data from the link provided [link to be provided][datadeform]. Then, open a Python terminal and run the following commands.

```python
from phybers.utils import deform
deform(imgdef= ‘id_acpc_dc2standard.nii’, infile=‘subject_raw.bundles’, outfile=‘subject_rawtoMNI.bundles’)
```
 > > ### _phybers.utils.sampling_
 > > > ### _Description_

The ***sampling*** sub-module performs a sampling of the fibers, recalculating their points using a defined number of equidistant points. The sampling sub-module is used in the preprocessing stage of the segmentation and clustering algorithms.

> > > ### _sampling Functions_

```python
def sampling(indir: str, npoints: int = 21, outdir: str) -> None
```
> > >### _sampling  Parameters_

The inputs are:
-	***indir***: input tractography dataset
-	***npoints***: number of sampling points (***n***)
-	***outdir***: path to save the sub-sampled fibers

The outputs files are:
-	The tractography dataset sampled at ***n*** equidistant points.

> > > ### _sampling Example_
To test `sampling()`,  download the data from the link provided [link to be provided][datasampling]. Then, open a Python terminal and run the following commands.

```python
from phybers.utils import sampling
sampling(indir= ‘test_allpoint.bundles’, npoints= 21, outdir= ‘test_21poits.bundles’)
```
 > > ### _phybers.utils.intersection_
 > > > ### _Description_

The bundle ***intersection*** sub-module calculates a similarity measure between two sets of brain fibers (fiber clusters or segmented bundles). It uses a maximum distance threshold to consider two fibers as similar. Both sets of fibers must be in the same space. First, a Euclidean distance matrix is calculated between the fibers of the two sets. Then, the maximum distance threshold is applied between fiber pairs and the number of fibers from one set that have a similar fibers in the other set are count, for both sets. The similarity measure yields a value between $0$ and $100\%$. 
> > > ### _intersection Functions_

```python
def intersection(dir_fib1: str, dir_fib2: str, outdir: str, d_th: float = 10.0) -> tuple[float, float]
```
> > >### _intersection  Parameters_

The inputs are:
- ***dir_fib1***: path of the first fiber bundle
- ***dir_fib2***: path of the second fiber bundle
- ***outdir***: path to save the distance matrix
- 	***d_th***: istance threshold in millimeters used to consider similar two fibers

The outputs files are:
-	`intersection()` returns a tuple with the intersection percentage. The first value indicates the percentage of intersection of the first set of fibers compared to the second set of fibers, and the second value indicates the reverse scenario, intersection of the second set of fibers compared to the first set of fibers.

> > > ### _intersection Example_
To test `intersection()`,  download the data from the link provided [link to be provided][dataintersection]. Then, open a Python terminal and run the following commands.

```python
from phybers.utils import intersection
result_inter=intersection (dir_fib1='fibers1.bundles', ir_fib2='fibers2.bundles', outdir='inter_result', d_th=10.0)

print(' intersection fibers1 with fibers2', result_inter [0])
print(' intersection fibers2 with fibers1', result_inter [1])
```

 > > ### _phybers.utils.postprocessing_
 > > > ### _Description_

***Postprocessing*** sub-module contains a set of algorithms that can be applied on the results of clustering and segmentation algorithms. This algorithm constructs a Pandas library object (Dataframe), where each key corresponds to the name of the fiber set (cluster or segmented fascicle), followed by measures defined on the fiber set such as: size (number of fibers), intra-set distance and mean length (in $mm$). It can be used to perform single or multiple feature filtering on the clustering or segmentation results. 

> > > ### _postprocessing Functions_

```python
def postprocessing(in_directory: string) -> None
```
> > >### _postprocessing  Parameters_

The inputs are:
- 	***in_directory***: directory where the segmentation or clustering result is located

The outputs files are:
-	`postprocessing()` return "pandas": DataFrame output, which has the following list of keys:
*'id_bundle': bundle identifier, 'sizes': number of fibers in the bundle ,'lens': centroid length per bundle, 'intra_min': manimum intra-bundle Euclidean distance and intra_mean': mean intra-bundle Euclidean distance*

> > > ### _postprocessing Example_
To test `postprocessing()`,  download the data from the link provided [link to be provided][datapostprocessing]. Then, open a Python terminal and run the following commands.

```python
from phybers.utils import postprocessing
postprocessing(in_directory=string)
```
#
 > ## _phybers.fibervis_

 > > ### _Description_
The tractography files can be rendered with lines or cilynders. In the case of lines, the software loads the streamlines with a fixed normal per vertex, which correspond to the normalized direction for the particular segment of the streamline. Furthermore, a phong lighting algorithm [ABrainVis][abrainvis] is implemented in a vertex shader to compute the color fetched for the streamline. The MRI data is rendered by using specific shaders for slice visualization and volume rendering. Meshes can be displayed using points, wireframes or shaded triangles. The user interface (GUI) allows viewing several objects simultaneously, performing camera operations (zoom, rotate and motion), modifying material properties (color and adding transparency) and applying linear transformation (zoom, rotate and motion) on the brain tractography.

*Fiber selection based on 3D ROIs*

This function allows users to extract bundles using 3D objects and labeled 3D images, creating a point-based data structure for fast queries (called Octree). It is based on storing points inside a bounding box with a capacity of N. When a node is filled and a new point is added, the node subdivides his bounding box in eight new nodes (no overlapping each other) and the points are moved in the new nodes. The resulting selected fiber for each object can be used into logical mathematical operations (and, or, xor, not). This allows the use of multiple ROIs in order to find fibers that connect some areas, while excluding others that are selected by others areas.

> > ### _Functions_

```python
def start_fibervis() -> None
```

> > ### Example
To test `fibervis()`, download the data from the links provided above. Then, open a Python terminal and run the following commands:

```python
from phybers. fibervis import start_fibervis
start_fibervis()
```

`fibervis()`is installed as a program, which allows you to run it through the command line in Windows or Ubuntu. To execute it on both platforms, use the following command:

```python
fibervis
```
For your convenience in using `fibervis()`, a video demonstrating all its features is now accessible through the following link
[link to be provided][video]

   [Pg2012]: <https://doi.org/10.1016/j.neuroimage.2012.02.071>
   [LN2017]: <https://link.springer.com/article/10.1007/s12021-016-9316-7>
   [An2019]: <https://doi.org/10.1109/ISBI.2019.8759208>
   [cl2017]: <https://doi.org/10.3389/fninf.2017.00073>
   [cl2022]: <https://doi.org/10.1016/j.neuroimage.2022.119550>
   [zhang2018]: <https://doi.org/10.1016/j.neuroimage.2018.06.027>
   [va2020]: <https://doi.org/10.1016/j.neuroimage.2020.117070>
   [od2007]: <https://doi.org/10.1109/TMI.2007.906785>
   [abrainvis]: <https://doi.org/10.1186/s12938-021-00909-0>
   [datafiberseg]: <https://link.>
   [datahclust]: <https://link.>
   [dataffclust]: <https://link.>
   [datadeform]: <https://link.>
   [dataintersection]: <https://link.>
   [datasampling]: <https://link.>
   [datapostprocessing]: <https://link.>
   [video]: <https://link.>
   
