from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph_nx import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize, flood_fill

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_2"

images = load_image_stack(folder_path)

# ## Code Process and Execution

floodf = flood_fill(images, (40, 267, 470), 0, tolerance=235)
floodf2 = flood_fill(floodf, (48, 282, 64), 0, tolerance=90)
floodf3 = flood_fill(floodf2, (43, 251, 105), 0, tolerance=200)
floodf4 = flood_fill(floodf3, (0, 367, 52), 0, tolerance=35)

split_flood = split_and_process_stack(floodf4, 250, 5)

skel = skeletonize(split_flood)

# ### For visualization purposes only

blend = blended(skel)
single_download(blend, "./Test/Images/OP_2_skel.png")

# ### Graph generation

graph = Graph(skel)
graph.set_root((26, 391, 1))
graph.create_graph()
root = graph.get_root()
g_root = (0.72501,391.08,25)
print(f"OP_2 GOLD STANDARD ROOT: {g_root}\nTEST ROOT: {root}")

distances, paths = graph.apply_dijkstra_and_label_nodes()

print(f"from dijkstra -> len(distances): {len(distances)}, len(paths): {len(paths)}")

print("SWC generated:",graph.save_to_swc("./Test/OP_2.swc"))
