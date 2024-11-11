class SWCDataset:
    def __init__(self):
        self.data = []
    
    def add_point(self, id, type, x, y, z, width, parent_id):
        self.data.append({
            'id': id,
            'type': type,
            'x': x,
            'y': y,
            'z': z,
            'width': width,
            'parent_id': parent_id
        })
    
    def calculate_moving_average(self, window_size=3):
        moving_avg = []
        
        for i in range(len(self.data)):
            start = max(0, i - window_size // 2)
            end = min(len(self.data), i + window_size // 2 + 1)
            
            avg_x = sum(point['x'] for point in self.data[start:end]) / (end - start)
            avg_y = sum(point['y'] for point in self.data[start:end]) / (end - start)
            avg_z = sum(point['z'] for point in self.data[start:end]) / (end - start)
            
            moving_avg.append((avg_x, avg_y, avg_z))
        
        return moving_avg
    
    def add_new_point(self, new_data):
        last_id = self.data[-1]['id']
        new_id = last_id + 1
        
        new_parent_id = last_id if len(self.data) > 0 else -1
        
        self.data.append({
            'id': new_id,
            'type': new_data['type'],
            'x': new_data['x'],
            'y': new_data['y'],
            'z': new_data['z'],
            'width': new_data['width'],
            'parent_id': new_parent_id
        })
    
    def print_results(self):
        print("# ID type x y z width parentID")
        for point in self.data:
            print(f"{point['id']} {point['type']} {point['x']} {point['y']} {point['z']} {point['width']} {point['parent_id']}")
        
        moving_avg = self.calculate_moving_average()
        print("\nMoving Average:")
        for i, avg in enumerate(moving_avg):
            print(f"Point {i+1}: ({avg[0]:.2f}, {avg[1]:.2f}, {avg[2]:.2f})")

# Uso da classe
swc = SWCDataset()

# Adicionar pontos iniciais
for id, data in enumerate([
    {'type': 9, 'x': 29, 'y': 433, 'z': 2, 'width': 1.2},
    {'type': 9, 'x': 30, 'y': 432, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 31, 'y': 432, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 32, 'y': 431, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 33, 'y': 430, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 33, 'y': 429, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 32, 'y': 428, 'z': 3, 'width': 1.2},
    {'type': 9, 'x': 32, 'y': 427, 'z': 4, 'width': 1.2},
    {'type': 9, 'x': 33, 'y': 426, 'z': 4, 'width': 1.2},
    {'type': 9, 'x': 33, 'y': 425, 'z': 4, 'width': 1.2},
    {'type': 9, 'x': 32, 'y': 424, 'z': 4, 'width': 1.2}
], start=1):
    swc.add_point(id, **data)

# Imprimir resultados iniciais
print("Dados iniciais:")
swc.print_results()

# Adicionar um novo ponto
new_point = {'type': 9, 'x': 31, 'y': 423, 'z': 4, 'width': 1.2}
swc.add_new_point(new_point)

# Imprimir resultados após adição do novo ponto
print("\n\nDados após adição de novo ponto:")
swc.print_results()
