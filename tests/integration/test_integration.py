import subprocess
import shlex
import sys
from pathlib import Path
import tempfile
import unittest
import os
import configparser


from push_file_to_object_storage import copy_object_to_s3_storage

basedir = Path(__file__).parent
FILES = basedir


def mkdtemp():
    if sys.version_info < (3, 10):  # ignore_cleanup_errors was added in 3.10
        return tempfile.TemporaryDirectory()
    else:
        return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def mkdir_testfiles(localmodule, test):
    """Keep the test files in a labeled test dir for easy reference"""
    testroot = Path(localmodule) / '.testfiles'
    testroot.mkdir(exist_ok=True)
    testdir = testroot / unittest.TestCase.id(test)
    testdir.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(dir=testdir))

def docker_exists():
    docker_command = "docker info"
    try:
        subprocess.check_output(shlex.split(docker_command))
    except Exception:
        return False
    else:
        return True
    

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        os.chdir(basedir)
        self._td = mkdtemp()
        self.testdir = self._td.name

    def tearDown(self):
        self._td.cleanup()

    @unittest.skipUnless(docker_exists(), "Docker is not available")
    def test_copy_object_to_s3_storage_with_rclone_and_minio(self):
        # This test shows how a file can be copied to s3 without using mocks
        try:
            from testcontainers.minio import MinioContainer
        except ImportError:
            self.skipTest('Requires testcontainers.minio to run')
        with MinioContainer(image="quay.io/minio/minio:latest") as minio:
            # Set up minio bukcet
            client = minio.get_client()
            client.make_bucket('test-bucket')
            host_ip = minio.get_config()['endpoint']

            # Set up file to be copied
            os.chdir(self.testdir)
            fake_file = "sample.txt"
            with open(fake_file, "w") as fp:
                fp.write('this is a text file for testing')

            # write out config for test use
            rclone_config = configparser.ConfigParser()
            rclone_config.add_section("test-minio-config")
            rclone_config.set("test-minio-config", "type", "s3")
            rclone_config.set("test-minio-config", "provider", "Minio")
            rclone_config.set("test-minio-config", "endpoint", "http://" + host_ip)
            rclone_config.set("test-minio-config", "acl", "public-read")
            rclone_config.set("test-minio-config", "env_auth", "true")
            rclone_config.set("test-minio-config", "region", "us-east-1")
            rclone_config.set("test-minio-config", "access_key_id", "minioadmin")
            rclone_config.set("test-minio-config", "secret_access_key", "minioadmin")

            rclone_config_path = Path('rclone_config_path')
            rclone_config_path.mkdir(parents=True, exist_ok=True)
            rclone_file = rclone_config_path / 'rclone-minio.conf'
            with open(rclone_file, "w", encoding="utf-8") as configfile:
                rclone_config.write(configfile)

            # set up config for run
            awsbucket = "test-bucket"

            # setup parameters for this test run
            object = fake_file
            rclone_config = "test-minio-config"
            path_to_rclone_config = str(rclone_file)

            # call function
            copy_object_to_s3_storage(awsbucket, object, rclone_config, path_to_rclone_config)
            bucket_content = client.list_objects('test-bucket', recursive=True)
            files_in_bucket = {obj.object_name for obj in bucket_content}
            print(files_in_bucket)
        self.assertEqual(
            files_in_bucket,
            {'sample.txt'},
        )