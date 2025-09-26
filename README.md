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
python3 -m unittest discover tests/unit
```

The integration test can be run with the command

```bash
python3 -m unittest discover tests/integration
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)