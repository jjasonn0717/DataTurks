import json
import random
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="split dataset")
    parser.add_argument('--input', required=True, help="the path to the jsonl dataset")
    parser.add_argument('--output_prefix', required=True, help="the prefix for the output jsonl files")
    parser.add_argument('--worker_profiles', required=True, help="the path to the worker profiles")
    parser.add_argument('--seed', type=int, default=0, help="random seed")
    args = parser.parse_args()

    random.seed(args.seed)

    with open(args.input, 'r') as f:
        data = []
        for idx, line in enumerate(f):
            line = line.strip()
            data.append(line)
        data = data[:100]
        print(f"load {len(data)} from {args.input}")

    with open(args.worker_profiles) as f:
        worker_profiles = json.load(f)

    random.shuffle(data)

    step = len(data) // len(worker_profiles) + 1
    start = 0
    for email in worker_profiles:
        worker_id = worker_profiles[email]['worker_id']
        output_path = f"{args.output_prefix}_{worker_id}.jsonl"
        with open(output_path, 'w') as f:
            end = min(start+step, len(data))
            print(f"dump data from {start} to {end-1} to {output_path}")
            for line in data[start:end]:
                f.write(line+'\n')
        start += step
