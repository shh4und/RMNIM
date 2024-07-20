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

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_2"
images = load_tif_stack(folder_path)

bilateral = bilateral_blur(images, 11, 200, 200)
# bilateral = bilateral_blur(images, 9, 200, 200) Score: 0,781

threshold1 = mean_threshold(bilateral, 50)
binary1 = simple_binary(bilateral, threshold1)
seg1 = segment(bilateral, binary1)

threshold2 = mean_threshold(seg1, 50)
binary2 = simple_binary(seg1, threshold2)
# ### Graph generation

skel = img_as_ubyte(skeletonize(binary2))

graph = Graph(skel)
graph.set_root((26, 391, 1))
graph.create_graph()
root = list(graph.get_root())[::-1]
g_root = (0.72501,391.08,25)
print(f"OP_1 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {tuple(root)}")

mst = graph.apply_dfs_and_label_nodes()

graph.save_to_swc(mst,"./Test/OP_2.swc")