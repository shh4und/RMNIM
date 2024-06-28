from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from ip.utils import *
from skimage.morphology import skeletonize
from skimage.util import img_as_ubyte
from scipy import ndimage

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_1"

images = load_image_stack(folder_path)

# ## Code Process and Execution

bilateral = bilateral_blur(images, 9, 175, 175)

threshold1 = mean_threshold(bilateral)
binary1 = simple_binary(bilateral, threshold1)
seg1 = segment(bilateral, binary1)

threshold2 = mean_threshold(seg1)
binary2 = simple_binary(seg1, threshold2)

strel3 = create_spherical_strel(3)
eroded3 = ndimage.binary_erosion(binary2, strel3)


skel_op3 = img_as_ubyte(skeletonize(eroded3))
# ### For visualization purposes only

# blend = blended(skel)
# single_download(blend, "./Test/Images/OP_1_skel.png")

# ### Graph generation

graph = Graph(skel_op3)
graph.set_root((3, 429, 34))
graph.create_graph()
root = graph.get_root()
g_root = (30.979,429.04,0)
print(f"OP_1 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

mst = graph.apply_dfs_and_label_nodes()

graph.save_to_swc("./Test/OP_1.swc")
