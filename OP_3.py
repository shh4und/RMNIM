from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from skimage.util import img_as_ubyte
from skimage.morphology import skeletonize

# Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_3"

images = load_tif_stack(folder_path)

##Code Process and Execution

bilateral = bilateral_blur(images, 11, 225, 225)

threshold1 = mean_threshold(bilateral,5)
binary1 = simple_binary(bilateral, threshold1)
seg1 = segment(bilateral, binary1)

threshold2 = mean_threshold(seg1, 5)
binary2 = simple_binary(seg1, threshold2)
skel = img_as_ubyte(skeletonize(binary2))
##For visualization purposes only

blend = blended(skel)
single_download(blend, "./Test/Images/OP_3_skel.png")



##Graph generation

graph = Graph(skel)
graph.set_root((37, 180, 95))
graph.create_graph()
root = graph.get_root()
g_root = (93.742,179,38)
print(f"OP_3 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

mst = graph.apply_dfs_and_label_nodes()
graph.save_to_swc(mst,"./Test/OP_3.swc")
