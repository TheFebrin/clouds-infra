from google.cloud import pubsub_v1

project_id = "chmurki-329715"
topic_id = "broker1"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)


X = [200, 400, 600, 800, 1000]
Y = [100, 200, 300, 400, 500]

for number_of_iterations, population_size in zip(X, Y):
    data = f'{number_of_iterations} {population_size}'
    # Data must be a bytestring
    data = data.encode("utf-8")
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data)
    print('Future result: ', future.result())

    print(f"Published message {data} to {topic_path}.")