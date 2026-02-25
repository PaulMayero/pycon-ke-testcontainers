import os
import subprocess


def copy_object_to_s3_storage(bucket, object, rclone_config, path_to_rclone_config=None):
    """
    Upload an object on file path to S3 Storage
    bucket -> S3 storage bucket
    object -> File to push to bucket
    rclone_config -> using default rclone config at /.config/rclone/rclone.conf
    """
    # get pwd
    current_dir = os.getcwd()
    complete_object_path = current_dir + "/" +object
    if os.path.exists(complete_object_path):
        object_path = complete_object_path
    else:
        raise Exception("File not found")

    # get path to default rclone config
    if path_to_rclone_config is None:
        output = subprocess.check_output(['rclone', 'config', 'file'], text=True)
        default_config_path = output.split('\n')[-2]
        if os.path.exists(default_config_path):
            path = default_config_path
    else:
        # return complete path to rclone file
        if os.path.exists(path_to_rclone_config):
            path = path_to_rclone_config
    
    # Create complete rclone command
    rclone_sync_command = ["rclone", "copy"]
    if path:
        rclone_sync_command += ["--config", path]
    rclone_sync_command += ["--verbose"]
    complete_remote_path = f'{rclone_config}:{bucket}'
    cmd = rclone_sync_command + [ object_path, complete_remote_path ]
    print(cmd)
    if subprocess.call(cmd) != 0:
        raise Exception("Failed to push object to Bucket")
    print(f"Success! You have backed up {object} on {bucket}. Your data is safe!")

if __name__ == "__main__":
    copy_object_to_s3_storage("pycon-namibia", "qr-code.png","pycon-namibia-config")



