from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize

# Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_3"

images = load_image_stack(folder_path)

##Code Process and Execution

split = split_and_process_stack(images, 17, 3)

skel = skeletonize(split)

##For visualization purposes only

blend = blended(skel)
single_download(blend, "./Test/Images/OP_3_skel.png")

##Graph generation

graph = Graph(skel)
graph.set_root((38, 180, 94))
graph.create_graph()
root = graph.get_root()
g_root = (93.742,179,38)
print(f"OP_3 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

distances, paths = graph.apply_dijkstra_and_label_nodes()

print(f"from dijkstra -> len(distances): {len(distances)}, len(paths): {len(paths)}")

print("SWC generated:",graph.save_to_swc("./Test/OP_3.swc"))
