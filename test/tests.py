import contextlib  
import csv
import os  
import sys
import tempfile
import unittest
from unittest import mock

from raceresults import command_line as cmd
 
@contextlib.contextmanager  
def chdir(dirname=None):  
    curdir = os.getcwd()  
    try:  
        if dirname is not None:  
            os.chdir(dirname)  
        yield  
    finally:  
        os.chdir(curdir)

class TestSuite(unittest.TestCase):

    def create_membership_file(self, filename, members):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['FName', 'LName']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for member in members:
                fname, lname = member.split()
            writer.writerow({'FName': fname, 'LName': lname})

    def test_activerr_nj_mismatch(self):
        with tempfile.TemporaryDirectory() as tdir:
            with chdir(tdir):
                memb_file = os.path.join(tdir, 'test.csv')
                self.create_membership_file(memb_file, ['Lauren Rome'])
                args = ['', '-y', '2014', '-m', '8', '-d', '25', '30',
                        '--ml', memb_file, '-o', 'results.html']
                with mock.patch('sys.argv', args):
                    cmd.run_active()

                with open('results.html') as fptr:
                    output = fptr.read()
                
                self.assertTrue("Lauren Rome" in output)

    def test_bestrace(self):
        with tempfile.TemporaryDirectory() as tdir:
            with chdir(tdir):
                memb_file = os.path.join(tdir, 'test.csv')
                self.create_membership_file(memb_file, ['Aidan Walsh'])
                args = ['', '-y', '2015', '-m', '1', '-d', '1', '1',
                        '--ml', memb_file, '-o', 'results.html']
                with mock.patch('sys.argv', args):
                    cmd.run_bestrace()

                with open('results.html') as fptr:
                    output = fptr.read()
                
                self.assertTrue("AIDAN WALSH" in output)

    def test_coolrunning(self):
        with tempfile.TemporaryDirectory() as tdir:
            with chdir(tdir):
                memb_file = os.path.join(tdir, 'test.csv')
                self.create_membership_file(memb_file, ['Dan Vassallo'])
                args = ['', '-y', '2015', '-m', '3', '-d', '8', '8',
                        '--ml', memb_file, '-o', 'results.html']
                with mock.patch('sys.argv', args):
                    cmd.run_coolrunning()

                with open('results.html') as fptr:
                    output = fptr.read()
                
                self.assertTrue("Dan Vassallo" in output)

    def test_compuscore(self):
        with tempfile.TemporaryDirectory() as tdir:
            with chdir(tdir):
                memb_file = os.path.join(tdir, 'test.csv')
                self.create_membership_file(memb_file, ['Jeff Pellis'])
                args = ['', '-y', '2015', '-m', '3', '-d', '7', '7',
                        '--ml', memb_file, '-o', 'results.html']
                with mock.patch('sys.argv', args):
                    cmd.run_compuscore()

                with open('results.html') as fptr:
                    output = fptr.read()
                
                self.assertTrue("2.Jeff Pellis" in output)

    def nyrr_base_run(self):
        with tempfile.TemporaryDirectory() as tdir:
            with chdir(tdir):
                args = ['', '-y', '2014', '-m', '12', '-d', '13', '13',
                        '-o', 'results.html']
                with mock.patch('sys.argv', args):
                    cmd.run_nyrr()

                with open('results.html') as fptr:
                    output = fptr.read()
                
                return output

    def test_nyrr(self):
        output = self.nyrr_base_run()

        self.assertTrue("Redona" in output)
        self.assertTrue("Leah" in output)


    def test_nyrr_latin1_nbsp(self):
        """
        No latin-1 nbsp chars allowed.

        Apparently the nyrr web pages have some latin1 chars.  Make sure they
        are removed.
        """
        output = self.nyrr_base_run()

        self.assertTrue("\xa0" not in output)



