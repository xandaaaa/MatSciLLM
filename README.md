# MatSciLLM

**MatSciLLM** is primarly an LLM-based application designed for material science research, enabling content extraction and analysis from PDFs along with access to the [Materials Project](https://materialsproject.org) Database.

## Features

- **User Interface** - User-friendly chat interface with convenient PDF management.

- **Specific Question** - Extracts the most relevant content from all uploaded PDFs based on a provided query.

- **Every PDF** - Provides answers to the query for each PDF individually.

- **Database Access** - Retrieves all unique stable element combinations for a given material from [Materials Project](https://materialsproject.org) (expandable).

## Setup

This repository includes a Docker setup, which can be conveniently accessed using the provided Makefile.

> **Note:** Make sure Docker is installed.

1. **Add API Key**  
   Insert your [Materials Project API key](https://next-gen.materialsproject.org/api) into the `.env.example` file. This key is required for accessing the Materials Project API.

2. **Create `.env` File**  
   Copy `.env.example` to `.env` to set up environment variables. 
    ```bash 
    cp .env.example .env
    ```

3. **Build Docker Image**  
   Use the provided Makefile to build the Docker image.
   ```bash 
   make build
   ```

4. **Run Docker Container**  
   Start the project in a Docker container using the Makefile.
   ```bash 
   make up
   ```

5. **Stop Docker Container**  
   When finished, stop the Docker container.
   ```bash
   make down
   ```

    &nbsp;

> Alternatively, you can manage and run the container directly through the Docker Desktop app after building the image.