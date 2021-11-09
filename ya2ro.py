import argparse

if __name__ == "__main__":

    #----------------------------------------------------------------------------------
    # Handle arguments
    #----------------------------------------------------------------------------------

    parser = argparse.ArgumentParser(
        description='Human and machine readeable input as a yalm file and create RO-Object in jsonld and/or HTML view.')

    # Required positional argument
    parser.add_argument('-i','--input', type=str, required=True, nargs='+',
        help='Path of the required yalm input. Follow the documentation or the example given to see the structure of the file.')

    # Optional argument
    parser.add_argument('-o', '--output_directory', type=str, help='Output diretory.', default="output")
    
    # Optional argument
    parser.add_argument('-p', '--properties_file', type=str, help='Properties file name.', default="resources/properties.yaml")

    args = parser.parse_args()

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

    import properties
    from ro_html import ro_html
    from ro_jsonld import ro_jsonld
    from pathlib import Path

    list_data = []

    for input_yalm in args.input:

        #----------------------------------------------------------------------------------
        # Create RO objects and dump results
        #----------------------------------------------------------------------------------
        

        data = properties.init(
            properties_file = args.properties_file, 
            input_yalm = input_yalm, 
            output_directory_param = Path(args.output_directory, str(Path(input_yalm).stem))
            )

        list_data.append(data)
        
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
    
    if len(list_data) > 1:
        ro_html.create_landing_page(args.output_directory, list_data)

