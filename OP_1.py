
from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_1"

images = load_image_stack(folder_path)

# ## Code Process and Execution

threshold1 = mean_threshold(images, 15)
binary1 = simple_binary(images, threshold1)
seg = segment(images, binary1)
denoising = median_blur(seg, 5)
threshold2 = mean_threshold(denoising, 15)
binary2 = simple_binary(denoising, threshold2)

skel = skeletonize(binary2)
# ### For visualization purposes only

# blend = blended(skel)
# single_download(blend, "./Test/Images/OP_1_skel.png")

# ### Graph generation

graph = Graph(skel)
graph.set_root((2, 428, 33))
graph.create_graph()
root = list(graph.get_root())[::-1]
g_root = (30.979,429.04,0)
print(f"OP_1 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {tuple(root)}")

mst = graph.apply_dfs_and_label_nodes()

graph.save_to_swc("./Test/OP_1.swc")
