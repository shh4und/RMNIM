
class SWCFile:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
    
    def add_point(self, identity, structure_type, x, y, z, radius, parent_identity):
        if identity <= 0 or parent_identity >= identity or (parent_identity != -1 and parent_identity <= 0):
            raise ValueError("Invalid identity or parent_identity values")
        self.data.append((identity, structure_type, x, y, z, radius, parent_identity))
    
    def write_file(self):
        self.data.sort()
        with open(self.filename, 'w') as file:
            file.write("# SWC test pilot\n")
            for point in self.data:
                line = " ".join(map(str, point)) + "\n"
                file.write(line)
        print("SWC saved at:", self.filename)
        return True