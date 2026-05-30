# Модель: Оптимізація енергоспоживання готелю з використанням генетичних алгоритмів (5 семестр)
# Автор: Біяк Марсела, група АІ-231

from flask import Flask, request, jsonify
import random

app = Flask(__name__)

devices = [
    {"name": "Освітлення номерів", "power": 12, "critical": False, "comfort": 8},
    {"name": "Освітлення коридорів", "power": 8, "critical": True, "comfort": 7},
    {"name": "Кондиціонування", "power": 20, "critical": False, "comfort": 10},
    {"name": "Кухонне обладнання", "power": 18, "critical": True, "comfort": 6},
    {"name": "Пральня", "power": 15, "critical": False, "comfort": 4},
    {"name": "Ліфт", "power": 10, "critical": True, "comfort": 9},
    {"name": "Серверна", "power": 14, "critical": True, "comfort": 10},
    {"name": "Мультимедійні системи", "power": 7, "critical": False, "comfort": 5},
]

POP_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1


def create_individual():
    individual = []

    for d in devices:
        if d["critical"]:
            individual.append(1)
        else:
            individual.append(random.randint(0, 1))

    return individual


def fitness(individual, max_power):
    total_power = 0
    comfort_loss = 0
    penalty = 0

    for gene, device in zip(individual, devices):

        if gene == 1:
            total_power += device["power"]

        else:
            if device["critical"]:
                penalty += 1000

            comfort_loss += device["comfort"]

    if total_power > max_power:
        penalty += (total_power - max_power) * 50

    return total_power + comfort_loss * 2 + penalty


def select(population, max_power):
    a = random.choice(population)
    b = random.choice(population)

    if fitness(a, max_power) < fitness(b, max_power):
        return a
    else:
        return b


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)

    child = parent1[:point] + parent2[point:]

    for i in range(len(child)):
        if devices[i]["critical"]:
            child[i] = 1

    return child


def mutate(individual):

    for i in range(len(individual)):

        if not devices[i]["critical"]:

            if random.random() < MUTATION_RATE:
                individual[i] = 1 - individual[i]

    return individual


def genetic_algorithm(max_power):

    population = []

    for _ in range(POP_SIZE):
        population.append(create_individual())

    for _ in range(GENERATIONS):

        new_population = []

        for _ in range(POP_SIZE):

            parent1 = select(population, max_power)
            parent2 = select(population, max_power)

            child = crossover(parent1, parent2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    best = min(population, key=lambda x: fitness(x, max_power))

    return best


@app.route('/calculate', methods=['GET'])
def calculate():

    max_power = int(request.args.get('max_power', 70))

    best_solution = genetic_algorithm(max_power)

    result = []

    total_power = 0

    for state, device in zip(best_solution, devices):

        status = "УВІМКНЕНО" if state == 1 else "ВИМКНЕНО"

        result.append({
            "device": device["name"],
            "status": status
        })

        if state == 1:
            total_power += device["power"]

    return jsonify({
        "max_power": max_power,
        "total_power": total_power,
        "fitness": fitness(best_solution, max_power),
        "devices": result
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
