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

import argparse
import properties
import data_wrapper
from ro_html import ro_html
from ro_jsonld import ro_jsonld
from ro_landing_page import ro_landing_page

def main():

    #----------------------------------------------------------------------------------
    # Handle arguments
    #----------------------------------------------------------------------------------

    parser = argparse.ArgumentParser(
        description='Human and machine readeable input as a yalm file and create RO-Object in jsonld and/or HTML view.')

    group = parser.add_mutually_exclusive_group(required=True)

    # Required positional argument 
    group.add_argument('-i','--input', type=str, nargs='+',
        help='Path of the required yalm input. Follow the documentation or the example given to see the structure of the file.')

    # Required positional argument
    group.add_argument('-l','--landing_page', type=str,
        help='Path of a previous output folder using the ya2ro tool. This flag will make a landing page to make all the resources accesible.')

    # Optional argument
    parser.add_argument('-o', '--output_directory', type=str, help='Output diretory.', default="output")
    
    # Optional argument
    parser.add_argument('-p', '--properties_file', type=str, help='Properties file name.', default="resources/properties.yaml")

    args = parser.parse_args()

    properties.init(
        properties_file = args.properties_file, 
        output_directory_param = args.output_directory
        )
    
    if args.input:
        process_input(args.input)

    if args.landing_page:
        process_landing_page(args.landing_page)


def process_input(input_list):

    for input_yalm in input_list:

        #----------------------------------------------------------------------------------
        # Create RO objects and dump results
        #----------------------------------------------------------------------------------

        data = data_wrapper.load_yaml(input_yalm)
        
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

    rlanding = ro_landing_page(landing_page_directory)
    rlanding.create_landing_page()
    

if __name__ == "__main__":
    main()