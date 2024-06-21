# # === working code for gpt3.5 turbo =======
# import random
# from openai import OpenAI

# client = OpenAI()
# from data_structures import EvolutionUnit, Population
# from prompts import THINKING_STYLES
# from rich.console import Console

# console = Console()

# def zero_order_prompt_gen(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     prompt = f"{unit.M} An ordered list of 10 hints: "
#     response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
#     unit.P = response.choices[0].text.strip()
#     unit.history.append(unit.P)
#     return unit

# def zero_order_hypermutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     random_thinking_style = random.choice(THINKING_STYLES)
#     prompt = f"{unit.M} {random_thinking_style}. Elaborate this thinking style:"
#     response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
#     unit.M = response.choices[0].text.strip()
#     unit.history.append(unit.M)
#     return unit

# def lineage_based_mutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     population = kwargs.get('population')   
#     elites = population.elites
#     if not elites:
#         return unit

#     prompt_history = " ".join([e.P for e in elites])
#     prompt = f"GENOTYPES FOUND IN ASCENDING ORDER OF QUALITY: {prompt_history}. Generate a new task prompt:"
#     response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
#     new_prompt = response.choices[0].text.strip()
#     unit.P = new_prompt
#     unit.history.append(new_prompt)
#     return unit



# def mutate(population: Population) -> Population:
#     MUTATORS = [
#         zero_order_prompt_gen,
#         zero_order_hypermutation,
#         lineage_based_mutation
#     ]

#     indices = [i for i in range(len(population.units))]
#     random.shuffle(indices)
#     pairs = [indices[i:i+2] for i in range(0, len(indices), 2)]

#     for first_idx, second_idx in pairs:
#         first_unit = population.units[first_idx]
#         second_unit = population.units[second_idx] if second_idx < len(population.units) else None

#         # Determine which unit to mutate
#         better_unit, worse_unit_idx = (first_unit, second_idx) if first_unit.fitness >= second_unit.fitness else (second_unit, first_idx)
#         random_mutator = random.choice(MUTATORS)

#         kwargs = {'population': population}

#         console.print(f"[bold blue]Before Mutation:[/bold blue] {better_unit}", style="yellow")
#         mutated_unit  = random_mutator(better_unit, **kwargs)
#         console.print(f"[bold blue]After Mutation:[/bold blue] {better_unit}", style="yellow")

#         population.units[worse_unit_idx] = mutated_unit


#     return population


# ======= Code for davinci002 =====
# import random
# import openai
# from data_structures import EvolutionUnit, Population
# from prompts import THINKING_STYLES
# from rich.console import Console

# console = Console()
# openai.api_key = "sk-your-api-key"

# def zero_order_prompt_gen(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     prompt = f"{unit.M} An ordered list of 10 hints: "
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=prompt,
#         max_tokens=1000
#     )
#     unit.P = response.choices[0].text.strip()
#     unit.history.append(unit.P)
#     return unit

# def zero_order_hypermutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     random_thinking_style = random.choice(THINKING_STYLES)
#     prompt = f"{unit.M} {random_thinking_style}. Elaborate this thinking style:"
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=prompt,
#         max_tokens=1000
#     )
#     unit.M = response.choices[0].text.strip()
#     unit.history.append(unit.M)
#     return unit

# def lineage_based_mutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
#     population = kwargs.get('population')
#     elites = population.elites
#     if not elites:
#         return unit

#     prompt_history = " ".join([e.P for e in elites])
#     prompt = f"GENOTYPES FOUND IN ASCENDING ORDER OF QUALITY: {prompt_history}. Generate a new task prompt:"
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=prompt,
#         max_tokens=1000
#     )
#     new_prompt = response.choices[0].text.strip()
#     unit.P = new_prompt
#     unit.history.append(new_prompt)
#     return unit

# def mutate(population: Population) -> Population:
#     MUTATORS = [
#         zero_order_prompt_gen,
#         zero_order_hypermutation,
#         lineage_based_mutation
#     ]

#     indices = list(range(len(population.units)))
#     random.shuffle(indices)
#     pairs = [indices[i:i+2] for i in range(0, len(indices), 2)]

#     for pair in pairs:
#         first_idx = pair[0]
#         first_unit = population.units[first_idx]
        
#         if len(pair) == 2:
#             second_idx = pair[1]
#             second_unit = population.units[second_idx]
#         else:
#             second_unit = None

#         if second_unit:
#             better_unit, worse_unit_idx = (first_unit, second_idx) if first_unit.fitness >= second_unit.fitness else (second_unit, first_idx)
#         else:
#             better_unit, worse_unit_idx = first_unit, first_idx

#         random_mutator = random.choice(MUTATORS)

#         kwargs = {'population': population}

#         console.print(f"[bold blue]Before Mutation:[/bold blue] {better_unit}", style="yellow")
#         mutated_unit = random_mutator(better_unit, **kwargs)
#         console.print(f"[bold blue]After Mutation:[/bold blue] {mutated_unit}", style="yellow")

#         population.units[worse_unit_idx] = mutated_unit

#     return population


#trying for one shot
import random
from openai import OpenAI

client = OpenAI()
from data_structures import EvolutionUnit, Population
from prompts import THINKING_STYLES
from rich.console import Console

console = Console()

def zero_order_prompt_gen(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
    one_shot_question = unit.one_shot_example['question']
    one_shot_answer = unit.one_shot_example['answer']
    prompt = f"{unit.M} An ordered list of 10 hints: One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer}"
    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
    unit.P = response.choices[0].text.strip()
    unit.history.append(unit.P)
    return unit

def zero_order_hypermutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
    random_thinking_style = random.choice(THINKING_STYLES)
    one_shot_question = unit.one_shot_example['question']
    one_shot_answer = unit.one_shot_example['answer']
    prompt = f"{unit.M} {random_thinking_style}. Elaborate this thinking style: One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer}"
    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
    unit.M = response.choices[0].text.strip()
    unit.history.append(unit.M)
    return unit

def lineage_based_mutation(unit: EvolutionUnit, **kwargs) -> EvolutionUnit:
    population = kwargs.get('population')   
    elites = population.elites
    if not elites:
        return unit

    prompt_history = " ".join([e.P for e in elites])
    one_shot_question = unit.one_shot_example['question']
    one_shot_answer = unit.one_shot_example['answer']
    prompt = f"GENOTYPES FOUND IN ASCENDING ORDER OF QUALITY: {prompt_history}. Generate a new task prompt: One-Shot Example: Question: {one_shot_question} Answer: {one_shot_answer}"
    response = client.completions.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
    new_prompt = response.choices[0].text.strip()
    unit.P = new_prompt
    unit.history.append(new_prompt)
    return unit


def mutate(population: Population) -> Population:
    MUTATORS = [
        zero_order_prompt_gen,
        zero_order_hypermutation,
        lineage_based_mutation
    ]

    indices = [i for i in range(len(population.units))]
    random.shuffle(indices)
    pairs = [indices[i:i+2] for i in range(0, len(indices), 2)]

    for first_idx, second_idx in pairs:
        first_unit = population.units[first_idx]
        second_unit = population.units[second_idx] if second_idx < len(population.units) else None

        better_unit, worse_unit_idx = (first_unit, second_idx) if first_unit.fitness >= second_unit.fitness else (second_unit, first_idx)
        random_mutator = random.choice(MUTATORS)

        kwargs = {'population': population}

        console.print(f"[bold blue]Before Mutation:[/bold blue] {better_unit}", style="yellow")
        mutated_unit  = random_mutator(better_unit, **kwargs)
        console.print(f"[bold blue]After Mutation:[/bold blue] {better_unit}", style="yellow")

        population.units[worse_unit_idx] = mutated_unit

    return population
