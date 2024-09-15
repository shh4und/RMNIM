from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from skimage.util import img_as_ubyte
from skimage.morphology import skeletonize
from scipy import ndimage

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_4"
images = load_tif_stack(folder_path)

# ## Code Process and Execution

bilateral = bilateral_blur(images, 9, 175, 175)
threshold1 = mean_threshold(bilateral)
binary1 = simple_binary(bilateral, threshold1)
seg1 = segment(bilateral, binary1)

threshold2 = mean_threshold(seg1)
binary2 = simple_binary(seg1, threshold2)
eroded3d = img_as_ubyte(ndimage.binary_erosion(binary2))
skel = img_as_ubyte(skeletonize(eroded3d))
graph = Graph(skel)
graph.set_root((3, 504, 128))
graph.create_graph()
root = graph.get_root()
g_root = (128.2,504.37,0.3)
print(f"OP_1 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

mst = graph.apply_dfs_and_label_nodes()
graph.save_to_swc(mst,"./Test/OP_4MA.swc",1.2)
