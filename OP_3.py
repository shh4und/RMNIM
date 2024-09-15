from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from skimage.util import img_as_ubyte
from skimage.morphology import skeletonize
from scipy import ndimage

# Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_3"

images = load_tif_stack(folder_path)

##Code Process and Execution

bilateral = bilateral_blur(images, 11, 75, 50)

binary3 = simple_binary(bilateral, mean_threshold(bilateral,7))
seg1 = segment(bilateral, binary3)
threshold2 = mean_threshold(seg1)
binary3 = simple_binary(seg1, threshold2)
eroded = ndimage.binary_opening(binary3)

skel2 = img_as_ubyte(skeletonize(eroded))

##For visualization purposes only

# blend = blended(skel)
#single_download(blend, "./Test/Images/OP_3_skel.png")

# cv2_imshow([blended(eroded)])
cv2_imshow(blended(skel2))

##Graph generation

graph = Graph(skel2)
graph.set_root((37, 180, 95))
graph.create_graph()
root = graph.get_root()
g_root = (93.742,179,38)
print(f"OP_3 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

mst = graph.apply_dfs_and_label_nodes()
graph.save_to_swc(mst,"./Test/OP_3GB.swc")
