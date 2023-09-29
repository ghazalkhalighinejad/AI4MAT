import os
import json



def process_json(folder_path):
    for filename in os.listdir(folder_path):
        # get the first four characters of the filename
        # if it already exist in the processed folder then continue
        first_four_letters_of_filename = filename[:4]
        if not os.path.exists(f'processed_data/{first_four_letters_of_filename}'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as json_file:
                # Read the JSON file
                data = json.load(json_file)
                if "MATERIALS" not in data["PolymerNanocomposite"]:
                    continue
                if "Matrix" not in data["PolymerNanocomposite"]["MATERIALS"]:
                    continue
                if isinstance(data["PolymerNanocomposite"]["MATERIALS"]["Matrix"], list):
                    continue
                if isinstance(data["PolymerNanocomposite"]["MATERIALS"]["Matrix"]["MatrixComponent"], list):
                    continue
                matrix_chemical = data["PolymerNanocomposite"]["MATERIALS"]["Matrix"]["MatrixComponent"]["ChemicalName"]
                
                
                if "CHARACTERIZATION" not in data["PolymerNanocomposite"]:
                    continue
                print(data["PolymerNanocomposite"]["CHARACTERIZATION"])
                if "Transmission_Electron_Microscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Transmission_Electron_Microscopy"
                elif "Scanning_Electron_Microscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Scanning_Electron_Microscopy"
                elif "Atomic_Force_Microscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Atomic_Force_Microscopy"
                elif "Optical_Microscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Optical_Microscopy"
                elif "Fourier_Transform_Infrared_Spectroscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Fourier_Transform_Infrared_Spectroscopy"
                elif "Dielectric_and_Impedance_Spectroscopy_Analysis" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Dielectric_and_Impedance_Spectroscopy_Analysis"
                elif "Raman_Spectroscopy" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Raman_Spectroscopy"
                elif "Differential_Scanning_Calorimetry" in data["PolymerNanocomposite"]["CHARACTERIZATION"]:
                    char_section = "Differential_Scanning_Calorimetry"
                else: 
                    continue
                
                processing_method = None
                if "PROCESSING" in data["PolymerNanocomposite"]:
                    if "SolutionProcessing" in data["PolymerNanocomposite"]["PROCESSING"]:
                        processing_method = "Solution Processing"
                    elif "MeltMixing" in data["PolymerNanocomposite"]["PROCESSING"]:
                        processing_method = "Melt Mixing"
                    elif "In-SituPolymerization" in data["PolymerNanocomposite"]["PROCESSING"]:
                        processing_method = "In-SituPolymerization"
                    else:
                        continue
                else:
                    continue

                new_file_name = f"processed/" + first_four_letters_of_filename
                with open(new_file_name, "w") as new_file:
                    new_data = {
                        "matrix_chemical": matrix_chemical,
                        "char_section": char_section,
                        "processing_method": processing_method
                    }
                    print("new_data", new_data)
                    json.dump(new_data, new_file, indent=4)
              

    

if __name__ == '__main__':
    folder_path = '/usr/project/xtmp/gk126/nlp-for-materials/nlp-for-materials/AI4MAT/json_ground_truth/true_json'
    
    process_json(f"{folder_path}")
