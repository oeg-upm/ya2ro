import argparse
import os
from pathlib import Path

###################################################################################
# LOGO

print("""
                        ad888888b,                         
                       d8"     "88                         
                               a8P                         
8b       d8 ,adPPYYba,      ,d8P"  8b,dPPYba,  ,adPPYba,   
`8b     d8' ""     `Y8    a8P"     88P'   "Y8 a8"     "8a  
 `8b   d8'  ,adPPPPP88  a8P'       88         8b       d8  
  `8b,d8'   88,    ,88 d8"         88         "8a,   ,a8"  
    Y88'    `"8bbdP"Y8 88888888888 88          `"YbbdP"'   
    d8'                                                    
   d8' 
_________________________________________________________
    """)

def main():

    #----------------------------------------------------------------------------------
    # Handle arguments
    #----------------------------------------------------------------------------------


    parser = argparse.ArgumentParser(
        description="""Human and machine readable input as a yaml file and create RO-Object in jsonld and/or HTML view.
        Run 'ya2ro -configure GITHUB_PERSONAL_ACCESS_TOKEN' this the first time to configure ya2ro properly""")

    group = parser.add_mutually_exclusive_group(required=True)

    # Required positional argument 
    group.add_argument('-i','--input', type=str, metavar='YALM_PATH',
        help='Path of the required yaml input. Follow the documentation or the example given to see the structure of the file.')

    # Required positional argument 
    group.add_argument('-c','--configure', type=str, metavar='GITHUB_PERSONAL_ACCESS_TOKEN',
        help='Insert Github personal access token. Run this the first time to configure ya2ro properly.')

    # Required positional argument
    group.add_argument('-l','--landing_page', type=str, metavar='YA2RO_PREV_OUTPUT',
        help='Path of a previous output folder using the ya2ro tool. This flag will make a landing page to make all the resources accesible.')

    # Optional argument
    parser.add_argument('-o', '--output_directory', type=str, metavar='OUTPUT_DIR',
        help='Output diretory.', default="output")
    
    # Optional argument
    parser.add_argument('-p', '--properties_file', type=str, metavar='PROPERTIES_FILE',
        help='Properties file name.', default="resources/properties.yaml")

    # Optional argument
    parser.add_argument('-ns', '--no_somef', action='store_true',
         help='Disable SOMEF for a faster execution (software cards will not work).')

    args = parser.parse_args()
    
    if args.configure:
        configure_somef(args.configure)
        return

    from . import properties

    properties.init(
        properties_file = args.properties_file, 
        output_directory_param = args.output_directory,
        n_somef = args.no_somef
        )
    
    if args.input:
        process_yaml(args.input)

    if args.landing_page:
        process_landing_page(args.landing_page)




def process_yaml(yaml_folder_or_file_str):

    try:
        yaml_folder_or_file = Path(yaml_folder_or_file_str)
        yaml_list = []
    
        if yaml_folder_or_file.is_dir():

            for file in os.scandir(yaml_folder_or_file):
                if file.path.endswith(".yaml") and file.is_file():
                    yaml_list.append(str(Path(file)))

        else:

            yaml_list.append(str(yaml_folder_or_file))
    except:
        print(f"ERROR: -i, --input {yaml_folder_or_file_str} is not valid file or directory.")
        exit()

    from . import data_wrapper
    from .ro_html import ro_html
    from .ro_jsonld import ro_jsonld

    for yaml in yaml_list:

        #----------------------------------------------------------------------------------
        # Create RO objects and dump results
        #----------------------------------------------------------------------------------

        data = data_wrapper.load_yaml(yaml)
        
        # Just to improve the stdout
        print("")

        rhtml = ro_html()
        rhtml.load_data(data)
        rhtml.create_HTML_file()

        rjsonld = ro_jsonld()
        rjsonld.load_data(data)
        rjsonld.create_JSONLD_file()

        # Just to improve the stdout
        print("")


def process_landing_page(landing_page_directory):

    from .ro_landing_page import ro_landing_page

    rlanding = ro_landing_page(landing_page_directory)
    rlanding.create_landing_page()
    
def configure_somef(token):
    from somef import configuration
    print("Running initial configuration:")
    configuration.configure(authorization=token)

if __name__ == "__main__":
    main()