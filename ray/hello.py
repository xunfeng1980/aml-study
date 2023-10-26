import ray

ray.init(address='192.168.31.123:6379')

if __name__ == '__main__':
    # Define the square task.
    @ray.remote
    def square(x):
        return x * x


    # Launch four parallel square tasks.
    futures = [square.remote(i) for i in range(4)]

    # Retrieve results.
    print(ray.get(futures))