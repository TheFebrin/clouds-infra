from typing import List
import numpy as np
import time
import datetime
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from google.cloud import firestore


def PMX(ind1, ind2):
    n = len(ind1)
    a, b = np.random.randint(0, n, 2)
    if a > b:
        a, b = b, a
        
    chld1 = [-1] * n
    chld2 = [-1] * n
    
    chld1[a: b + 1] = ind1[a: b + 1]
    chld2[a: b + 1] = ind2[a: b + 1]
    
    used1 = set(chld1)
    used2 = set(chld2)
    
    lookup1 = [0] * n
    lookup2 = [0] * n
    
    for i in range(n):
        lookup1[ind1[i]] = i
        lookup2[ind2[i]] = i
    
    r = [i for i in range(a + 1)] + [i for i in range(b, n)]
    
    for i in r:
        if chld1[i] == -1:
            if ind2[i] not in used1:
                chld1[i] = ind2[i]
                used1.add(ind2[i])
                
        if chld2[i] == -1:
            if ind1[i] not in used2:
                chld2[i] = ind1[i]
                used2.add(ind1[i])
    
    for i in r:
        if chld1[i] == -1:
            candidate = ind2[i]
            while candidate in used1:
                candidate = ind2[lookup1[candidate]]
            chld1[i] = candidate
            used1.add(candidate)
                
        if chld2[i] == -1:
            candidate = ind1[i]
            while candidate in used2:
                candidate = ind1[lookup2[candidate]]
            chld2[i] = candidate
            used2.add(candidate)

    return chld1, chld2 


def reverse_sequence_mutation(p):
    a = np.random.choice(len(p), 2, False)
    i, j = a.min(), a.max()
    q = p.copy()
    q[i: j + 1] = q[i: j + 1][::-1]
    return q


def calculate_distance(p: List[int], A: np.ndarray) -> float:
    s = 0.0
    for i in range(len(p)):
        s += A[p[i - 1], p[i]]
    return s


def SGA(
    chromosome_length,
    distance_matrix,
    number_of_iterations,
    population_size, 
    crossover_probability=0.95, 
    mutation_probability=0.25,
    crossover=PMX,
    mutation=reverse_sequence_mutation,
    objective_function=calculate_distance,
    debug=True
):    
    number_of_offspring = population_size
    time0 = time.time()

    best_objective_value = np.Inf
    best_chromosome = np.zeros((1, chromosome_length))
    cost_values = []

    # generating an initial population
    current_population = np.zeros((population_size, chromosome_length), dtype=np.int64)
    for i in range(population_size):
        current_population[i, :] = np.random.permutation(chromosome_length)

    # evaluating the objective function on the current population
    objective_values = np.zeros(population_size)
    for i in range(population_size):
        objective_values[i] = objective_function(current_population[i, :], distance_matrix)

    for t in range(number_of_iterations):

        # selecting the parent indices by the roulette wheel method
        fitness_values = objective_values.max() - objective_values
        if fitness_values.sum() > 0:
            fitness_values = fitness_values / fitness_values.sum() 
        else:
            fitness_values = np.ones(population_size) / population_size
        parent_indices = np.random.choice(population_size, number_of_offspring, True, fitness_values).astype(np.int64)

        # creating the children population
        children_population = np.zeros((number_of_offspring, chromosome_length), dtype=np.int64)
        for i in range(int(number_of_offspring/2)):
            if np.random.random() < crossover_probability:
                children_population[2*i, :], children_population[2*i+1, :] = \
                crossover(current_population[parent_indices[2*i], :].copy(), current_population[parent_indices[2*i+1], :].copy())
            else:
                children_population[2*i, :] = current_population[parent_indices[2*i], :].copy()
                children_population[2*i+1, :] = current_population[parent_indices[2*i+1]].copy()

        if np.mod(number_of_offspring, 2) == 1:
            children_population[-1, :] = current_population[parent_indices[-1], :]

        # mutating the children population
        for i in range(number_of_offspring):
            if np.random.random() < mutation_probability:
                children_population[i, :] = mutation(children_population[i, :])

        # evaluating the objective function on the children population
        children_objective_values = np.zeros(number_of_offspring)
        for i in range(number_of_offspring):
            children_objective_values[i] = objective_function(children_population[i, :], distance_matrix)

        # replacing the current population by (Mu + Lambda) Replacement
        objective_values = np.hstack([objective_values, children_objective_values])
        current_population = np.vstack([current_population, children_population])

        I = np.argsort(objective_values)
        current_population = current_population[I[:population_size], :]
        objective_values = objective_values[I[:population_size]]

        # recording some statistics
        if best_objective_value < objective_values[0]:
            best_objective_value = objective_values[0]
            best_chromosome = current_population[0, :]

        cost_values.append([objective_values.min(), objective_values.mean(), objective_values.max()])
        if t % 10 == 0 and debug:
            print(f'iter: {t},\
     || time: {time.time() - time0:.2f},\
     || min: {objective_values.min():.2f},\
     || mean: {objective_values.mean():.2f},\
     || max: {objective_values.max():.2f},\
     || std: {objective_values.std():.2f}')
            
    return cost_values, current_population


def solve_berlin(number_of_iterations: int, population_size: int):
    # BERLIN52
    n = 52
    print(f'Solving Berlin 52 TSP')
    print(f'number_of_iterations = {number_of_iterations}')
    print(f'population_size = {population_size}')

    coords = np.array([565.0, 575.0, 25.0, 185.0, 345.0, 750.0, 945.0, 685.0, 845.0, 655.0, 880.0, 660.0, 25.0, 230.0, 525.0, 1000.0, 580.0, 1175.0, 650.0, 1130.0, 1605.0, 620.0, 1220.0, 580.0, 1465.0, 200.0, 1530.0, 5.0, 845.0, 680.0, 725.0, 370.0, 145.0, 665.0, 415.0, 635.0, 510.0, 875.0, 560.0, 365.0, 300.0, 465.0, 520.0, 585.0, 480.0, 415.0, 835.0, 625.0, 975.0, 580.0, 1215.0, 245.0, 1320.0, 315.0, 1250.0, 400.0, 660.0, 180.0, 410.0, 250.0, 420.0, 555.0, 575.0, 665.0, 1150.0, 1160.0, 700.0, 580.0, 685.0, 595.0, 685.0, 610.0, 770.0, 610.0, 795.0, 645.0, 720.0, 635.0, 760.0, 650.0, 475.0, 960.0, 95.0, 260.0, 875.0, 920.0, 700.0, 500.0, 555.0, 815.0, 830.0, 485.0, 1170.0, 65.0, 830.0, 610.0, 605.0, 625.0, 595.0, 360.0, 1340.0, 725.0, 1740.0, 245.0])
    coords = coords.reshape(n, 2)

    A = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A[i, j] = np.sqrt(((coords[i, :] - coords[j, :]) ** 2).sum())

    # print('Distance matrix shape:\n', A.shape)

    p = [0, 48, 31, 44, 18, 40,  7,  8,  9, 42, 32, 50, 10, 51, 13, 12, 46, 25, 26, 27, 11, 24,  3,  5, 14,  4, 23, 47, 37, 36, 39, 38, 35, 34, 33, 43, 45, 15, 28, 49, 19, 22, 29,  1,  6, 41, 20, 16,  2, 17, 30, 21]
    # print('Optimal solution:\n', p)
    print('Optimal distance:', calculate_distance(p=p, A=A))

    print('\n\n=== SOLVING THE PROBLEM ===\n\n')
    start = time.time()

    cost_values, current_population = SGA(
        number_of_iterations=number_of_iterations,
        population_size=population_size,
        chromosome_length=n,
        distance_matrix=A,
        debug=False,
    )

    found_distance: float = calculate_distance(p=current_population[-1], A=A)
    print('Found best distance', found_distance)
    print(f'Took: {time.time() - start :.2f}s')
    # Add a new document with calculations summary
    date: str = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    db = firestore.Client()
    doc_ref = db.collection('berlin52').document(date + f'-iters-{number_of_iterations}')
    doc_ref.set({
        'number_of_iterations': number_of_iterations,
        'population_size': population_size,
        'found_distance': found_distance,
        'time_elapsed': time.time() - start,
    })


def main():
    project_id = "chmurki-329715"
    topic_id = "broker1"
    subscription_id = "sub1"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received message: {message}.")
        number_of_iterations, population_size = map(int, message.data.decode('UTF-8').split())
        solve_berlin(
            number_of_iterations=number_of_iterations, 
            population_size=population_size,
        )
        message.ack()
        print('Message acked\n')

    flow_control = pubsub_v1.types.FlowControl(max_messages=1)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control
    )
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


if __name__ == '__main__':
    main()