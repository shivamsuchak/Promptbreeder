# Promptbreeder

# Prompt Breeder

## Overview

Prompt Breeder is a Python project designed to generate and evolve prompts for language models, such as OpenAI's GPT-3.5-turbo, to solve specific tasks. It employs a genetic algorithm approach, evolving the prompts over several generations to optimize their performance.

## Files

1. `run_prompt.py`: The main script that orchestrates the prompt generation and evolution process.
2. `mutations.py`: Contains the mutation functions used to evolve the prompts.
3. `utils.py`: Utility functions used for reading datasets and processing model responses.

## Requirements

- Python 3.7+
- OpenAI Python SDK
- Rich (for enhanced logging and console output)
- Other standard Python libraries (argparse, typing, os, random, logging)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/prompt-breeder.git
    cd prompt-breeder
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Prepare the `gsm8k_sampled.jsonl` dataset and place it in the project directory.

2. Run the `run_prompt.py` script with the desired parameters:
    ```bash
    python run_prompt.py -ts 2 -mp 2 -p "Solve the math word problem, giving your answer as an arabic numeral." -e 10 -n 5
    ```

### Parameters

- `-ts`, `--num_thinking_styles`: Number of thinking styles to use (default: 2).
- `-mp`, `--num_mutation_prompts`: Number of mutation prompts to use (default: 2).
- `-p`, `--problem_statement`: The problem statement to be solved (default: "Solve the math word problem, giving your answer as an arabic numeral.").
- `-e`, `--num_evals`: Number of evaluations for each unit (default: 10).
- `-n`, `--simulations`: Number of generations/simulations to run (default: 5).

## Script Details

### `run_prompt.py`

This script contains the main logic for creating the initial population of prompts, running the evolutionary algorithm, and evaluating the fitness of each prompt.

- **create_population**: Initializes the population with specified thinking styles and mutation prompts.
- **init_run**: Generates initial task prompts and evaluates their fitness.
- **evaluate_fitness**: Assesses the accuracy of the prompts based on a sample of questions.
- **run_for_n**: Runs the evolutionary algorithm for `n` generations.
- **main**: Parses command-line arguments and starts the prompt breeding process.

### `mutations.py`

Defines the mutation strategies for evolving the prompts.

- **zero_order_prompt_gen**: Generates a new prompt using a zero-order strategy.
- **zero_order_hypermutation**: Applies a hypermutation to the thinking style.
- **lineage_based_mutation**: Creates a new prompt based on the history of elite prompts.
- **mutate**: Applies mutations to the population and replaces less fit units with mutated ones.

### `utils.py`

Contains utility functions for reading datasets and processing model responses.

- **read_jsonl**: Reads a JSONL file and returns a list of dictionaries.
- **gsm_extract_answer**: Extracts the answer from the completion text.
- **check_answer_in_response**: Checks if the expected answer is present in the model's response.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project utilizes OpenAI's GPT-3.5-turbo model. Special thanks to the developers of the Rich library for providing enhanced logging and console output.

## Contact

For any inquiries, please contact [yourname@example.com](mailto:yourname@example.com).
