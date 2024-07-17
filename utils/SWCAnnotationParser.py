import os

def modify_swc_file(file_path: str, modifications: set) -> None:
    """Modifies the SWC file based on the provided modifications set.

    Args:
        file_path (str): swc filepath
        modifications (set): modification set
    """
    modified_lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        if "TEST" in lines[0].strip().upper():
            print(">> Test SWC file")
            for line in lines:
                # Skip header lines
                if line.startswith("#"):
                    modified_lines.append(line)
                    continue
                parts = line.strip().split()  # Remove trailing newline and split
                parts[1] = str(9)

                # Check if this node needs modification
                for mod_id in modifications:
                    # For extra nodes
                    x, y, z = map(float, mod_id)
                    if (
                        float(parts[2]) == x
                        and float(parts[3]) == y
                        and float(parts[4]) == z
                    ):
                        parts[1] = str(11)
                        break

                modified_line = (
                    " ".join(parts) + "\n"
                )  # Reconstruct line with newline character
                modified_lines.append(modified_line)
        else:
            print(">> Gold Standard SWC file")
            for line in lines:
                # Skip header lines
                if line.startswith("#"):
                    modified_lines.append(line)
                    continue
                parts = line.strip().split()  # Remove trailing newline and split
                parts[1] = str(8)
                # Check if this node needs modification
                for mod_id in modifications:
                    # For missing nodes
                    x, y, z = map(float, mod_id.split(","))
                    if (
                        float(parts[2]) == x
                        and float(parts[3]) == y
                        and float(parts[4]) == z
                    ):
                        parts[1] = str(10)
                        break

                modified_line = (
                    " ".join(parts) + "\n"
                )  # Reconstruct line with newline character
                modified_lines.append(modified_line)

    # Write modifications back to the file
    with open(os.path.splitext(file_path)[0] + "_annotations.swc", "w") as file:
        file.writelines(modified_lines)


# Example usage
extra_nodes_modifications = {
    (369, 189, 34),
    (367, 190, 32),
    (370, 187, 33),
    (367, 189, 31),
    (343, 186, 21),
    (344, 194, 21),
    (419, 228, 45),
    (428, 195, 43),
    (431, 195, 42),
    (444, 195, 42),
    (441, 170, 36),
    (424, 181, 39),
    (436, 189, 39),
    (391, 201, 39),
    (172, 304, 49),
    (134, 232, 46),
    (38, 316, 28),
    (39, 352, 20)
}

missing_nodes_modifications = {
    "162.31,287.69,45.783",
    "139.05,238.32,48.066",
    "143.43,249.91,47.56",
    "196.86,290.71,45.058",
    "168.8,308.81,49.101",
    "222.6,257.72,47.306",
    "238.28,293.86,50.124",
    "227.14,260.14,53.556",
    "278.03,267.54,54.02",
    "286.98,240.85,51.595",
    "360.14,199.9,34.862",
    "361.67,202.69,25.009",
    "346.87,183.34,21.932",
    "357.22,217.74,20.939",
    "313.1,193.03,11.845",
    "367.29,194.24,23.594",
    "379.23,171.28,31.186",
    "375.36,162.99,35.178",
    "384.98,173.88,40.212",
    "371.86,173.61,21.128",
    "383.79,144.59,29.896",
    "399.69,149.05,26.999",
    "407.17,145.83,24.038",
    "408.98,145.8,21.985",
    "413.05,149.17,17.596",
    "424.38,154.91,17.738",
    "425.81,156.4,16.012",
    "409.48,145.69,22.171",
    "396.16,147.76,21.88",
    "414.84,145.64,23.683",
    "415.95,145.67,25.155",
    "399.46,148.56,27.321",
    "418.58,145.86,30.015",
    "399.67,148.33,27.697",
    "423.09,156.34,22.273",
    "423.83,155.67,19.811",
    "430.84,157.45,20.945",
    "432.92,154.57,18.856",
    "437.09,162.98,18.676",
    "417.86,163.64,40.641",
    "385.81,195.72,37.436",
    "378.27,182.82,37.982",
    "388.67,195.91,37.752",
    "419.86,222.95,45.823",
    "420.75,231.55,45.874",
    "420.98,173.93,39.978",
    "438.71,199.4,43.766",
    "444.94,171.71,34.787",
    "449.26,199.21,42.961",
    "408.78,186.01,43.983",
}

modify_swc_file("Test/backup/OP_1.swc", extra_nodes_modifications)
modify_swc_file("Test/backup/OP_1GOLD.swc", missing_nodes_modifications)
