from pathlib import Path
import properties as p

def create_htaccess(output_datafolder):

    htaccess = """
    # Turn off MultiViews
    Options -MultiViews

    AddType application/ld+json .json

    RewriteEngine on

    RewriteBase /""" + str(output_datafolder) + """

    # Rewrite rule to serve HTML
    RewriteCond %{HTTP_ACCEPT} !application/rdf\+xml.*(text/html|application/xhtml\+xml)
    RewriteCond %{HTTP_ACCEPT} text/html [OR]
    RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
    RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*
    RewriteRule ^$ ./index-en.html [R=303,L]

    # Rewrite rule to serve JSON-LD content from the vocabulary URI if requested
    RewriteCond %{HTTP_ACCEPT} application/ld\+json
    RewriteRule ^$ ./ro-crate.json [R=303,L]
    """


    with open(Path(output_datafolder, ".htaccess"), "w") as text_file:
        text_file.write(htaccess)

def create_htaccess_landing(output_directory):

    htaccess = """
    # Turn off MultiViews
    Options -MultiViews

    RewriteEngine on

    RewriteBase /""" + str(output_directory) + """

    # Rewrite rule to serve HTML
    RewriteCond %{HTTP_ACCEPT} !application/rdf\+xml.*(text/html|application/xhtml\+xml)
    RewriteCond %{HTTP_ACCEPT} text/html [OR]
    RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
    RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*
    RewriteRule ^$ ./""" + str(p.properties["output_html_landing"]) + """ [R=303,L]

    """

    with open(Path(output_directory, ".htaccess"), "w") as text_file:
        text_file.write(htaccess)
    