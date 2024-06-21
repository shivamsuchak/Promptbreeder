
import argparse
from typing import List
import os
import openai
from rich import print

from data_structures import EvolutionUnit, Population
from gsm8k_utils import gsm_extract_answer, read_jsonl, check_answer_in_response
from mutations import mutate
from prompts import MUTATION_PROMPTS, THINKING_STYLES

from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
import logging
import random

# Setup rich logging
install()
console = Console()
logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(console=console)])


def create_population(tp_set: List[str], mutator_set: List[str], problem_description: str, one_shot_example: dict) -> Population:
    """Creates a population based on the provided sets of thinking styles and mutation prompts."""
    units = [EvolutionUnit(T=t, M=m, P='', fitness=0, history=[]) 
             for t in tp_set for m in mutator_set]
    for unit in units:
        unit.one_shot_example = one_shot_example  # Add one-shot example to each unit
    return Population(size=len(units), age=0, problem_description=problem_description, units=units)


def init_run(population: Population, gsm8k_examples: List[dict], num_evals: int) -> Population:
    # Generate initial task prompts
    for unit in population.units:
        one_shot_question = unit.one_shot_example['question']
        one_shot_answer = unit.one_shot_example['answer']
        prompt = f"{unit.T} {unit.M} INSTRUCTION: {population.problem_description} One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer} INSTRUCTION MUTANT = "
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a {unit.M} assistant."},
                {"role": "user", "content": f"Solve the {unit.T} problem: {population.problem_description} One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer}"}
            ]
        )
        unit.P = response.choices[0].message.content

    # Evaluate fitness of each unit
    evaluate_fitness(population, gsm8k_examples, num_evals)

    return population


def evaluate_fitness(population: Population, gsm8k_examples: List[dict], num_evals: int) -> Population:
    elite_fitness = -1
    current_elite = None

    examples = random.sample(gsm8k_examples, num_evals)

    for unit in population.units:
        unit.fitness = 0

        for example in examples:
            one_shot_question = unit.one_shot_example['question']
            one_shot_answer = unit.one_shot_example['answer']
            prompt = unit.P + f" One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer} {example['question']}"
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600
            )

            model_answer = response.choices[0].message.content
            correct_answer = gsm_extract_answer(example['answer'])

            console.print(f"[bold cyan]LLM's Answer:[/bold cyan] {model_answer[-500:]}", style="cyan")
            console.print(f"[bold red]Actual Answer:[/bold red] {correct_answer}", style="red")

            if check_answer_in_response(model_answer, correct_answer):
                console.print("Correct!", style="green")
                unit.fitness += 1 / num_evals
            else:
                console.print("Incorrect!", style="red")

        if unit.fitness > elite_fitness:
            elite_fitness = unit.fitness
            current_elite = unit

    if current_elite:
        population.elites.append(current_elite)

    return population


def run_for_n(n: int, population: Population, gsm8k_examples: List[dict], num_evals:int) -> Population:
    for generation in range(n):
        print(f"[bold green]Running Generation {generation}[/bold green]")

        mutate(population)

        evaluate_fitness(population, gsm8k_examples, num_evals)

        max_fitness = max(unit.fitness for unit in population.units)
        print(f"[bold blue]Generation {generation} Summary:[/bold blue] Max Fitness: {max_fitness:.2f}")

    return population


def main(args):
    logger = logging.getLogger("Prompt Breeder")
    num_thinking_styles = args.num_thinking_styles
    num_mutation_prompts = args.num_mutation_prompts
    problem_statement = args.problem_statement

    thinking_styles = random.sample(THINKING_STYLES, num_thinking_styles)
    mutation_prompts = random.sample(MUTATION_PROMPTS, num_mutation_prompts)

    gsm8k_dataset = read_jsonl("./gsm8k_sampled.jsonl")
    openai.api_key = "your-api-key"

    one_shot_example = random.choice(gsm8k_dataset)  # Select one-shot example from dataset

    logger.info("Creating the initial population")
    population = create_population(mutation_prompts, thinking_styles, problem_statement, one_shot_example)
    print(population)

    init_run(population, gsm8k_dataset, args.num_evals)

    logger.info("Running the simulation")
    final_population = run_for_n(args.simulations, population, gsm8k_dataset, args.num_evals)
    print(final_population)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Prompt Breeder Algorithm.")
    parser.add_argument('-ts', '--num_thinking_styles', type=int, default=2, help="Number of thinking styles to use.")
    parser.add_argument('-mp', '--num_mutation_prompts', type=int, default=2, help="Number of mutation prompts to use.")
    parser.add_argument('-p', '--problem_statement', type=str, default="Solve the math word problem, giving your answer as an arabic numeral.")
    parser.add_argument('-e', '--num_evals', type=int, default=10, help="Number of evaluations for each unit.")
    parser.add_argument('-n', '--simulations', type=int, default=5, help="Number of generations/simulations to run.")

    args = parser.parse_args()
    main(args)
