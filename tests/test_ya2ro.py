from unittest import TestCase, mock
import unittest
import sys
from unittest import mock
from ya2ro import ya2ro
import pathlib
import os, shutil

@mock.patch('ya2ro.data_wrapper.metadata_parser.MetadataParser')
@mock.patch('ya2ro.data_wrapper.req_orcid.orcid')
@mock.patch('ya2ro.data_wrapper.req_doi.bib')
@mock.patch('ya2ro.data_wrapper.req_doi.dataset')
class test_ya2ro(TestCase):

    @classmethod
    def setUpClass(cls):
        global prev_dir, parent_dir
        prev_dir = os.getcwd()
        parent_dir = str(pathlib.Path(__file__).parent.resolve())
        os.chdir(parent_dir)
    
    @classmethod
    def tearDownClass(cls):
        global prev_dir
        os.chdir(prev_dir)

    def setUp(self):
        global parent_dir
        os.chdir(parent_dir)

    def tearDown(self):
        global parent_dir
        os.chdir(parent_dir)
        shutil.rmtree('out', ignore_errors=True)

    # TESTS
    ################################################

    def test_paper(self, doi_dataset, doi_bib, orcid, metadata_parser):
        apply_mock(doi_dataset, doi_bib, orcid, metadata_parser)
        os.chdir("input/")
        _set_args("-i","yamls/paper.yaml","-o","../out","-ns")
        ya2ro.main()

    def test_paper_doi(self, doi_dataset, doi_bib, orcid, metadata_parser):
        apply_mock(doi_dataset, doi_bib, orcid, metadata_parser)
        os.chdir("input/")
        _set_args("-i","yamls/paper_doi.yaml","-o","../out","-ns")
        ya2ro.main()
        

    def test_project(self, doi_dataset, doi_bib, orcid, metadata_parser):
        apply_mock(doi_dataset, doi_bib, orcid, metadata_parser)
        os.chdir("input/")
        _set_args("-i","yamls/project.yaml","-o","../out")
        ya2ro.main()


    def test_landing_page(self, doi_dataset, doi_bib, orcid, metadata_parser):
        apply_mock(doi_dataset, doi_bib, orcid, metadata_parser)
        os.chdir("input/")
        _set_args("-i","yamls/paper.yaml","-o","../out","-ns")
        ya2ro.main()

        _set_args("-i","yamls/paper_doi.yaml","-o","../out","-ns")
        ya2ro.main()

        _set_args("-i","yamls/project.yaml","-o","../out","-ns")
        ya2ro.main()

        global parent_dir
        os.chdir(parent_dir)
        _set_args("-l","out")
        ya2ro.main()

# AUX
################################################

def _set_args(*args):
    sys.argv = [sys.argv[0]]+list(args)
    print(sys.argv)

def apply_mock(doi_dataset, doi_bib, orcid, metadata_parser):
        doi_dataset.return_value = mock_doi_dataset()
        doi_bib.return_value = mock_doi_bib()
        orcid.return_value = mock_orcid()
        metadata_parser.return_value = mock_metadata_parser()

# Mock classes
################################################

class mock_doi_dataset(object):

    def get_name():
        return "Mock dataset name"

    def get_author(self):
        return "Mock author name"

    def get_description(self):
        return "Mock description"

    def get_license(self):
        return "Mock license"

class mock_doi_bib(object):
    
    def get_title(self):
        return "Mock title"
    
    def get_authors(self):
        return ["Mock author"]

    def get_summary(self):
        return "Mock summary"

    def get_citation(self):
        return "Mock citation"
    
    def get_bibtext(self):
        return "Mock bibtext"

class mock_orcid(object):

    def get_full_name(self):
        return "Mock name"

    def get_webs(self):
        return ["http://mock_web.com"]

    def get_affiliation(self):
        return ["Mock aff", "Mock aff 2"]
        
    def get_bio(self):
        return "Mock bio"

class mock_metadata_parser(object):

    def get_metadata():
        return "Mock metadata"

if __name__ == '__main__':
    unittest.main()
 