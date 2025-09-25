import os
from unittest import mock
from pathlib import Path
import tempfile
import sys
import unittest
import shutil
import configparser

basedir = Path(__file__).parent
FILES = basedir

from push_file_to_object_storage import copy_object_to_s3_storage


def mkdtemp():
    if sys.version_info < (3, 10):  # ignore_cleanup_errors was added in 3.10
        return tempfile.TemporaryDirectory()
    else:
        return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)

def _mock_rclone_config_file(cmd, text):  # pylint: disable=unused-argument
    """Mock output from rclone 1.60.1 but with nonexistent conf file."""
    return "Configuration file doesn't exist, but rclone will use this path:\n/nonexistent/rclone.conf\n"


class DeployTest(unittest.TestCase):

    def setUp(self):
        os.chdir(basedir)
        self._td = mkdtemp()
        self.testdir = self._td.name

    def tearDown(self):
        self._td.cleanup()

    @unittest.skipUnless(shutil.which('rclone'), 'requires rclone')
    def test_copy_object_to_s3_storage(self):
        os.chdir(self.testdir)
        fake_file = "sample.txt"
        with open(fake_file, "w") as fp:
            fp.write('this is a text file for testing')
        
        # write out a fake rclone config

        rclone_config = configparser.ConfigParser()
        rclone_config.add_section("test-local-config")
        rclone_config.set("test-local-config", "type", "local")

        rclone_config_path = Path('rclone_config_path')
        rclone_config_path.mkdir(parents=True, exist_ok=True)
        rclone_file = rclone_config_path / 'rclone.conf'
        with open(rclone_file, 'w') as configfile:
            rclone_config.write(configfile)

        # setup parameters for this test run
        s3_bucket = 'test_bucket_folder'
        object = fake_file
        rclone_config = "test-local-config"
        path_to_rclone_config = str(rclone_file)
        

        # write out destination path
        destination = Path(f'{s3_bucket}')
        destination.mkdir(parents=True, exist_ok=True)
        dest_apk = Path(destination) / fake_file
        self.assertFalse(dest_apk.is_file())
        copy_object_to_s3_storage(s3_bucket, object, rclone_config, path_to_rclone_config)
        self.assertTrue(dest_apk.is_file())
