# Better integration testing with TestContainers

This Repo shows how to use [TestContainers](https://testcontainers.com/)
for Integration and CI testing

## Set UP

To follow along with this example. Clone the repo

```bash
git clone git@github.com:PaulMayero/pycon-ke-testcontainers.git
```

## Usage

To follow along, ensure that [Docker](https://docs.docker.com/engine/install/)
and [Rclone](https://rclone.org/) are installed on your system.

Once the repo has been cloned, the unit tests can be run with the command

```bash
python3 -m unittest discover tests/unit -v
```

The integration test can be run with the command

```bash
virtualenv3 venv/
source venv/bin/activate
pip install testcontainers[minio]
python3 -m unittest discover tests/integration -v
```

The repository has support for [Github Actions](https://github.com/features/actions)
that run on push.   
To run Github actions locally, use [act](https://nektosact.com/).
Install act as per this
[documentation](https://nektosact.com/installation/index.html).  
Once the installation is complete, at the root of this repository run ```act```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
