# Prompt Breeder

## Overview

Prompt Breeder is a Python-based project designed to iteratively improve prompt generation for language models, inspired by the genetic algorithm approach used in DeepMind's Prompt Breeder. By simulating evolutionary processes, this project aims to refine and optimize prompts to enhance the performance of models like OpenAI's GPT-3.5-turbo in solving specific tasks. This involves generating an initial population of prompts, evaluating their effectiveness, and evolving them through mutations across multiple generations.


## Files

1. `run_prompt_breeder.py`: The main script that orchestrates the prompt generation and evolution process.
2. `mutations.py`: Contains the mutation functions used to evolve the prompts.
3. `utils.py`: Utility functions used for reading datasets and processing model responses.

## Requirements

- Python 3.7+
- OpenAI Python SDK
- Rich (for enhanced logging and console output)
- Other standard Python libraries (argparse, typing, os, random, logging)


## Usage

1. Prepare the `gsm8k_sampled.jsonl` dataset and place it in the project directory.

2. Run the `run_prompt_breeder.py` script with the desired parameters:
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
