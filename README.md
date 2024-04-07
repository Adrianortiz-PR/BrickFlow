# Lego API Project

This project is designed to read data from a TXT file, import it into MongoDB using a Python script, and then serve the data through a Go API.

## Directory Structure

```markdown
lego_api_project/
│
├── python/
│   ├── scrapper.py
│   └── import_data.py
│
├── go/
│   ├── go.sum
│   ├── go.mod
│   └── main.go
│
│
└── README.md
```

## Setup and Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your_username/lego_api_project.git
    cd lego_api_project
    ```

2. **Run Python Script to import data:**
    ```bash
   pythin import_data.py
    ```
3. **Run Go script:**
    ```bash
  run go main.go
    ```

4. **Access the API:**
    The API will be available at `http://localhost:8080`.

## Usage

- **Importing Data:**
    Modify the `lego_sets.txt` file in the `python` directory to include your Lego set data. Then, run the Python script to import the data into MongoDB.


- **Viewing Lego Sets:**
    You can view all Lego sets by accessing `http://localhost:8080/sets` in your browser or API testing tool.

- **Viewing a Specific Lego Set:**
    To view a specific Lego set, use the set number in the endpoint `http://localhost:8080/sets/{set_number}`.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
