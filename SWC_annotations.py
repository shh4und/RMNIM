def modify_swc_file(file_path:str, modifications:dict):
    """Modifies the SWC file based on the provided modifications dictionary.
    
    Args:
        file_path (str): swc filepath
        modifications (dict): modification dictionary
    """
    modified_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            # Skip header lines
            if line.startswith('#'):
                modified_lines.append(line)
                continue
            
            parts = line.strip().split()  # Remove trailing newline and split
            id_ = int(parts[0])
            
            # Check if this node needs modification
            for mod_id, new_type in modifications.items():
                if isinstance(mod_id, tuple):  # For extra nodes
                    x, y, z = map(float, mod_id)
                    if float(parts[2]) == x and float(parts[3]) == y and float(parts[4]) == z:
                        parts[1] = str(new_type)
                        break
                else:  # For missing nodes
                    x, y, z = map(float, mod_id.split(','))
                    if float(parts[2]) == x and float(parts[3]) == y and float(parts[4]) == z:
                        parts[1] = str(new_type)
                        break
            
            modified_line = ' '.join(parts) + '\n'  # Reconstruct line with newline character
            modified_lines.append(modified_line)
    
    # Write modifications back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)
# Example usage
extra_nodes_modifications = {
    (369,189,34): 3,
    (367,190,32): 3,
    (370,187,33): 3,
    (367,189,31): 3,
    (343,186,21): 3,
    (344,194,21): 3,
    (419,228,45): 3,
    (428,195,43): 3,
    (431,195,42): 3,
    (444,195,42): 3,
    (441,170,36): 3,
    (424,181,39): 3,
    (436,189,39): 3,
    (391,201,39): 3,
    (172,304,49): 3,
    (134,232,46): 3,
    (38,316,28): 3,
    (39,352,20): 3,
}

missing_nodes_modifications = {
    '162.31,287.69,45.783': 0,
    '139.05,238.32,48.066': 0,
    '143.43,249.91,47.56': 0,
    '196.86,290.71,45.058': 0,
    '168.8,308.81,49.101': 0,
    '222.6,257.72,47.306': 0,
    '238.28,293.86,50.124': 0,
    '227.14,260.14,53.556': 0,
    '278.03,267.54,54.02': 0,
    '286.98,240.85,51.595': 0,
    '360.14,199.9,34.862': 0,
    '361.67,202.69,25.009': 0,
    '346.87,183.34,21.932': 0,
    '357.22,217.74,20.939': 0,
    '313.1,193.03,11.845': 0,
    '367.29,194.24,23.594': 0,
    '379.23,171.28,31.186': 0,
    '375.36,162.99,35.178': 0,
    '384.98,173.88,40.212': 0,
    '371.86,173.61,21.128': 0,
    '383.79,144.59,29.896': 0,
    '399.69,149.05,26.999': 0,
    '407.17,145.83,24.038': 0,
    '408.98,145.8,21.985': 0,
    '413.05,149.17,17.596': 0,
    '424.38,154.91,17.738': 0,
    '425.81,156.4,16.012': 0,
    '409.48,145.69,22.171': 0,
    '396.16,147.76,21.88': 0,
    '414.84,145.64,23.683': 0,
    '415.95,145.67,25.155': 0,
    '399.46,148.56,27.321': 0,
    '418.58,145.86,30.015': 0,
    '399.67,148.33,27.697': 0,
    '423.09,156.34,22.273': 0,
    '423.83,155.67,19.811': 0,
    '430.84,157.45,20.945': 0,
    '432.92,154.57,18.856': 0,
    '437.09,162.98,18.676': 0,
    '417.86,163.64,40.641': 0,
    '385.81,195.72,37.436': 0,
    '378.27,182.82,37.982': 0,
    '388.67,195.91,37.752': 0,
    '419.86,222.95,45.823': 0,
    '420.75,231.55,45.874': 0,
    '420.98,173.93,39.978': 0,
    '438.71,199.4,43.766': 0,
    '444.94,171.71,34.787': 0,
    '449.26,199.21,42.961': 0,
    '408.78,186.01,43.983': 0,
}

modify_swc_file('Test/OP_1.swc', extra_nodes_modifications)
modify_swc_file('Test/OP_1GOLD.swc', missing_nodes_modifications)