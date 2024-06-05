
from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_4"

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

blend = blended(skel)
single_download(blend, "./Test/Images/OP_4_skel.png")

# ### Graph generation

graph = Graph(skel)
graph.set_root()
graph.create_graph()
root = graph.get_root()
g_root = (128.2,504.37,0.3)
print(f"OP_4 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

distances, paths = graph.apply_dijkstra_and_label_nodes()

print(len(distances), len(paths))

print("SWC generated:",graph.save_to_swc("./Test/OP_4.swc"))
