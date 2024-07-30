# Scaling Synthetic Data Generation

---
> REDACTED
>
> Jul XX, 2024
---

There is one unchanging constant in machine learning: "data is king." But what happens when you work in a field where the king doesn't always want to get out of bed every morning?

Welcome to neuroimaging, where data is not only hard to come by, but also requries a ton of space[^1].

Many have stood up to challenge this lack of data by inventing methods to generate synthetic data -- SynthSeg, SynthStrip, Synth, etc. They work really well[^2], but it has

<p align="center">.
<p align="center">.
<p align="center">.

---

<br>

## I. Issues

> If you'd like to skip ahead to the tutorial, go to section II.
>
> If you'd like to skip ahead to Wirehead's internal workings, go to section VII.
---

In late 2023, we at TReNDS attempted to make use of one such generator, [SynthSeg](https://arxiv.org/abs/2107.09559), to replicate the original results by training a MeshNet on 300,000 synthetic samples[^3]. However, early into the experimentation process, we noted three key things:

1. **Generation time** was quite significant (2 seconds per sample on our A40). Generating that many samples using their setup (train -> generate) would have taken us **hundreds of hours.**
2. **Data size was massive**, the papers report training on 300,000 samples, which would have been 91 terabytes at 32 bit precision 
3. **Hardware was greatly underutilized**. glancing at nvtop showed us that our gpus would be barely used during sample generation, before peaking for about 5 seconds while training on a new batch. On average, we got just **around 30% GPU utilization**


We could solve these issues by deploying the generator in parallel, but that posed its own set of issues:
- **Where would we store the data?** We still only had that much space on the cluster, and storing all of them at once would be infeasible. Some kind of **cache** was necessary
- **How would we coordinate these distributed generators?** We had SLURM, and could spin up 20 generators on the spot whenever we wanted, but it's nontrivial to figure out how to make this process sync up with the training process.
- **How would we maintain high GPU utilization for training?** The problem was clear -- Our GPUs would idle if they didn't have a sample to train on. Perfectly syncing up the throughput of generation to training is practically impossible, and overloading the training job with more samples than it needs would be wasteful of compute. So a workaround had to be figured out.

---

<br>

## II. TLDR (how to solve this problem without thinking about it)

> In short, we made Wirehead, a distributed, async cache that lets you arbitrarily scale your synthetic data generation. It does this with no net storage overhead, and minimal compute requirements.
>
> If you'd like to follow along the unit tests and examples from our repo, go [here](https://github.com/neuroneural/wirehead).
---

### 1. Install MongoDB

This is the onlty real dependency we have for wirehead. Here are some ways to get it up and running on a local instance or a cluster.

- [Ubuntu Setup](#a-quick-mongodb-setup-ubuntu)
- [macOS Setup](#b-quick-mongodb-setup-macos)
- [Singularity Setup](https://medium.com/@tholaday777/run-a-mongodb-docker-image-as-a-singularity-container-service-e68322df7abc)

**important note:** the following instructions are for development and testing purposes only. for production deployments, please refer to the [official mongodb documentation](https://www.mongodb.com/docs/manual/administration/install-community/) for secure and proper installation guidelines.

#### a. Quick MongoDB Setup ([Ubuntu](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)):

```bash
sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

```bash
# Run MongoDB
sudo systemctl start mongod
```

```bash
# Stop MongoDB
sudo systemctl stop mongod
```

#### b. Quick MongoDB Setup ([MacOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)):

Install [homebrew](https://brew.sh/) if you haven't
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
```

```bash
# Run MongoDB
brew services start mongodb-community@7.0
```

```bash
# Stop MongoDB
brew services stop mongodb-community@7.0
```

#### c. Singularity setup

Refer to [this excellent guide](https://medium.com/@tholaday777/run-a-mongodb-docker-image-as-a-singularity-container-service-e68322df7abc) from Tristan Holoday 


### 2. Python environment setup

For SLURM usage, do be mindful of where your conda or venv is, and how to activate it, as we will need to reliably pass that through to our sbatch jobs.

```bash
# Note:
# python version doesn't necessarily have to be 3.10
# but this gives better support for some generation pipelines

# Conda
conda create -n wirehead python=3.10
conda activate wirehead

# venv
python3.10 -m venv wirehead 
source venv/bin/activate
```

### 3. Install wirehead

```bash
pip install wirehead
```

### 4. Doing a test run

The unit test lives in examples/unit
```
git clone git@github.com:neuroneural/wirehead.git
cd wirehead/examples/unit
```

Configure the config.yaml file
```yaml
MONGOHOST: "localhost" # hostname or ip of node hosting mongodb
DBNAME: "unit-test"    # name of database inside mongodb
SWAP_CAP: 10           # max size for write/read collection
```

**Important note:** If you're running MongoDB on a separate computer, you should make sure that it is accessible to wherever you've deployed wirehead. (This usually means contact your sysadmins). Verify with
```python
from pymongo import MongoClient
# replace with hostname=localhost and port=27017 for defaults on a local instance
print("MongoDB is accessible" if MongoClient(
    host="your_hostname",
    port=your_port, serverSelectionTimeoutMS=2000
    ).server_info() else "MongoDB is not accessible")
```

Run the test
```
chmod +x test.sh
./test.sh
```

If tests pass, you should get:
```
All tests passed successfully! 
```


---

<br>

## III. Configuration

>Deploying wirehead involves 3 main scripts (or utilities): A generator(s) (generator.py) a cache manager (manager.py) and a data fetcher (loader.py)
>
>All examples in this section can be found in wirehead/examples/unit
---

### 1. config.yaml

All three of these scripts source a single config.yaml file, which consists of:
```
MONGOHOST: "localhost"          # hostname or ip of node hosting mongodb
DBNAME: "unit-test"             # name of database inside mongodb
SWAP_CAP: 10                    # max size for write/read collection
```

as well as some advanced configs (explained in a later section)
```
SAMPLE: ["data", "label"]       # string key associated with your samples
WRITE_COLLECTION: "write"       # name of write collecion on mongodb 
READ_COLLECTION: "read"         # name of read collection 
COUNTER_COLLECTION: "counter"   # name of counter collection used to keep index
TEMP_COLLECTION: "temp"         # name of temporary collection for movement ops
CHUNKSIZE: 10                   # size of chunks in MB for chunking data
```

In order of increasing complexity, here's how to configure each component of wirehead

### 2. manager.py

This is the simplest, and doesn't have to be changed if you're running it as a standalone script.

WireheadManager doesn't consume much compute, and thus can be deployed anywhere you want.

The only thing you need to specify is the path to your config file (in this case, "config.yaml")
```
from wirehead import WireheadManager

if __name__ == "__main__":
    wirehead_runtime = WireheadManager(config_path="config.yaml")
    wirehead_runtime.run_manager()
```

### 3. loader.py

This script is provides a simple way to fetch a single sample from Wirehead

We provide two kinds of datasets for fetching dataL MongoheadDataset (dictionary-like) and MongoTupleheadDataset (tuple-like)

Similar to manager.py, it's pretty much plug and play, and you can insert this into anywhere you'd like in your regular training script. the only thing you need to specify is the path to your config file (again, it is "config.yaml" in this example)
```
import torch
from wirehead import MongoheadDataset, MongoTupleheadDataset

idx = [0]

dict_dataset = MongoheadDataset(config_path="config.yaml")
data = dataset[idx]
sample, label = data[0]['input'], data[0]['label']

tuple_dataset = MongoTupleheadDataset(config_path="config.yaml")
data = dataset[idx][0]
sample, label = data[0], data[1]
```

### 4. generator.py

This is the heart of the operation, and where some explanation has to be done:
```
import numpy as np
from wirehead import WireheadGenerator 

def create_generator():
    while True: 
        img = np.random.rand(256,256,256)
        lab = np.random.rand(256,256,256)
        yield (img, lab)

if __name__ == "__main__":
    brain_generator     = create_generator()
    wirehead_runtime    = WireheadGenerator(
        generator = brain_generator,
        config_path = "config.yaml" 
    )
    wirehead_runtime.run_generator()
```

Like the manager and dataset, you need to specify your config_path ("config.yaml" in this example)

But one thing that's different, is that now you also have to specify a [generator function](https://wiki.python.org/moin/Generators) which **yields** a tuple containing your data. In this case, that generator looks like:
```
def create_generator():
    while True: 
        img = np.random.rand(256,256,256)
        lab = np.random.rand(256,256,256)
        yield (img, lab)
```

Wirehead has to serialize the data before sending it off, and in this case we decided to use numpy ndarrays. If you instead wanted to use torch tensors or some other data type, make sure they're [serializable](https://docs.python.org/3/library/pickle.html) and live in the CPU before yielding them


Then, all you have to do is plug an instance of your generator function, and the path to your config file into WireheadGenerator
```
brain_generator     = create_generator()
wirehead_runtime    = WireheadGenerator(
    generator = brain_generator,
    config_path = "config.yaml" 
)
```

And then press play (this runs an infinite loop)
```
wirehead_runtime.run_generator()
```


If you'd prefer to generate only N samples instead of running an infinite loop, you can specify that in your generator function:
```
N = 10000
def create_generator():
    for _ in range(N):  # generate 10000 samples
        img = np.random.rand(256,256,256)
        lab = np.random.rand(256,256,256)
        yield (img, lab)
```

WireheadGenerator will continue to push samples to the write collection as long as there are samples to yield. If your generator function fails or otherwise stops yielding, WireheadGenerator will self terminate.

---

<br>

## IV. Deployment

>Wirehead can be deployed both locally and on a SLURM managed cluster. 
>
>This section will guide you through both deployment scenarios.
---

### 1. Local

For local deployment, you'll need to run three main components: the generator, the manager, and your training script (which uses the loader). Here's a step-by-step guide:

a. Start MongoDB:
   Ensure MongoDB is running on your local machine. If it's not already running, start it using the appropriate command for your operating system (e.g., `sudo systemctl start mongod` on Ubuntu).

b. Run the manager:
   In a terminal, navigate to your Wirehead directory and run:
   ```
   python manager.py
   ```

c. Run the generator:
   Open another terminal, navigate to your Wirehead directory, and run:
   ```
   python generator.py
   ```

d. Run your training script:
   In a third terminal, run your training script that uses the Wirehead loader.

Make sure all scripts are using the same configuration file (config.yaml) pointing to your local MongoDB instance.

### 2. SLURM

For deployment on a SLURM-managed cluster, you'll need to create SLURM job scripts for the manager and generator. Your training script will also need to be submitted as a SLURM job. Here's how to set it up:

a. Manager Job Script:
   Create a file named `manager_job.sh`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=wirehead_manager
   #SBATCH --nodes=1
   #SBATCH -c 2
   #SBATCH --mem=4g
   #SBATCH --output=./log/manager_output_%j.log
   #SBATCH --error=./log/manager_error_%j.log
   #SBATCH --time=24:00:00
   #SBATCH -p qTRDGPU
   #SBATCH -A psy53c17

   echo "Starting Wirehead Manager on $(hostname)"
   conda activate wirehead_dev
   python manager.py
   ```

b. Generator Job Script:
   Create a file named `generator_job.sh`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=wirehead_generator
   #SBATCH --nodes=1
   #SBATCH -c 16
   #SBATCH --mem=50g
   #SBATCH --gres=gpu:A40:1
   #SBATCH --output=./log/generate_output_%A_%a.log
   #SBATCH --error=./log/generate_error_%A_%a.log
   #SBATCH --time=06:00:00
   #SBATCH -p qTRDGPU
   #SBATCH -A psy53c17
   #SBATCH --array=0-2

   echo "This is a Wirehead generator job on $(hostname)"
   conda activate wirehead_dev
   python generator.py
   ```

c. Submit the jobs:
   First, submit the manager job:
   ```
   sbatch manager_job.sh
   ```

   Then, submit the generator job:
   ```
   sbatch generator_job.sh
   ```

d. Training Job:
   Modify your training script to use the Wirehead loader, and submit it as a SLURM job.

Notes on the SLURM configuration:

- The manager job is set to run for 24 hours. Adjust this time as needed for your workload.
- The generator job is set up as an array job (--array=0-2), which will create 3 identical jobs. This allows you to run multiple generators in parallel.
- Both jobs use the qTRDGPU partition and the psy53c17 account. Adjust these according to your cluster's configuration.
- The generator job requests an A40 GPU. Modify this according to your available hardware.
- Both jobs activate a conda environment named 'wirehead_dev'. Ensure this environment exists and contains all necessary dependencies.

Remember to modify the config.yaml file to point to the MongoDB instance on your cluster. You may need to work with your system administrators to ensure MongoDB is properly set up and accessible from your compute nodes.

By using this SLURM setup, you can easily scale your data generation across multiple nodes, significantly speeding up your workflow.

---

<br>

## V. Case study -- SynthSeg









---
<br>

## VI. Advanced userland tech

>So far, Wirehead might seem quite barebones, having basically just the minimum to function as a reliable distributed data structure. 
>
>We decided to leave many of the decisions (such as how to manage and schedule generators) to the end user. 
>
>Accommodating all the different ways a generator could be handled, or deployed, would have significantly bloated our code. 
---

However, that doesn't mean we're going to leave you out for dry.

Here are some advanced tech that we've found during testing to make your life a lot easier while scaling your synthetic data generators:

### 1. Slurm tricks

The first and most obvious one is to leverage many of the features that slurm provides out of the box to avoid having to having to heterogenize your generators.

- [Slurm arrays](https://marcc-hpc.github.io/tutorials/shortcourse_jobarrays.html) for scheduling parallel jobs

Example
```bash
#!/bin/bash

#SBATCH --job-name=wirehead
#SBATCH --nodes=1
#SBATCH --gres=gpu:A40:1
#SBATCH --array=0-19  # << this lets you run 20 jobs in parallel, indexed 0..19

python worker.py
```

You can also use the slurm worker_id (the index from the example above) within the python runtime. This is useful for selecting 
```python
import os
worker_id = os.getenv("SLURM_ARRAY_TASK_ID", "0")
training_seg = DATA_FILES[worker_id % len(DATA_FILES)] # selects a different segment to condition based on id
```

### 2. Running multiple python processes

Assuming you don't have ergregious memory leaks, you can also deploy multiple generators in parallel in multiple python processes[^7]
```bash
#!/bin/bash
                                                                               
#SBATCH ...
                                                                               
NUM_GENERATORS=8
conda init bash
conda activate wirehead
                                                                               
for i in $(seq 0 $((NUM_GENERATORS-1))); do
  python generator.py $NUM_GENERATORS $i &
  pids+=($!)
done
                                                                               
for pid in "${pids[@]}"; do
  wait $pid
done
```

### 3. Benchmarks and debugging

#### a. Fetching single samples
You can do this by using the MongoheadDataset class
``` 
(venv) examples/unit § python
Python 3.10.14 (main, Jul 12 2024, 17:45:26)
Type "help", "copyright", "credits" or "license" for more information.
>>> from wirehead import MongoheadDataset

>>> dataset = MongoheadDataset("config.yaml")
Dataset: config loaded from config.yaml
Dataset: Data is ready

>>> x, y = batch[0]['input'], batch[0]['label']

>>> x.shape, y.shape
(torch.Size([256, 256, 256]), torch.Size([256, 256, 256]))
```

#### b. WireheadManager will provide some logging information
```
Manager: SWAP!
    Time: 1722356716.8162937 
    Generated samples: 4800
    Documents deleted: 0
Manager: SWAP!
    Time: 1722356737.930378 
    Generated samples so far 4850
    Documents deleted: 10
```

#### c. How to interpret results

Every time there is a swap, the manager will log:
```
Time:               current unix time
Generated samples:  how many samples generated in total so far
Documents deleted:  how corrupted / incomplete samples were thrown away
```

You can use these logs to get some figures for benchmarking
```python
>>> 1722356737.930378-1722356716.8162937
21.114      # seconds between swaps
>>> 4850-4800
50          # samples between swaps 
>>> 50/21.114084243774414
2.368       # samples per second
>>> 21.114084243774414/50
0.422       # seconds per sample
```

---
<br>

## VII. How to solve these issues while thinking about it

> So we looked at these problem and realized: What we need is a **distributed[^4] circular[^5] cache[^6]**. We made one, and called it [Wirehead](https://github.com/neuroneural/wirehead)
---

Okay what do you need for a cache? You basically just need
1. A way to **put** data in
2. A way to **get** data out
3. A way to **swap** old data with fresh data

Why a cache? And not some other strategy? Well, a circular cache:
- Eliminates the storage issue. Using a cache means we toss out the data after we're done using it for training
- Provides a convenient way to deal with the coordination issue. Using a cache means that we have a way to hook up our many generators to our training job.
- Eliminates the issue of low GPU utilization[^7]. Our training job would always have samples to train on.

Now the thing though, is that writing distributed systems software is [hard](http://nil.csail.mit.edu/6.824/2020/). If we did this from scratch, it would likely crash and burn every 5 minutes.

So we didn't, and instead relied on some battle hardened enterprise software. Enter [MongoDB](https://www.mongodb.com/) -- distributed, non-blocking[^n], and basically nuclear proof[^n]. It was exactly what we needed.

So, all we have to do now is to write those three components, and let MongoDB handle the ugly details of distributed systems reliability.

---
<br>

## VIII. Wirehead Internals

### 1. Put

```
def generate_and_insert(self):
    """ Fetch from generator and inserts into mongodb """
    # 0. Fetch data from generator
    data = next(self.generator)
    # 1. Get the correct index for this current sample
    index = self.get_current_idx()
    # 2. <<<< Turn the data into chunks >>>>
    chunks = self.chunkify(data, index)
    # 3. Push to mongodb + error handling
    if index < self.swap_cap:
        self.push_chunks(chunks)
```

- What is index?
- What is chunkifying doing?
- Pushing, and guardrails

### 2. Get
```
def __getitem__(self, batch):
    """
    Fetch all samples for ids in the batch and return as tuples
    """
    # 1. Get chunk indeces of samples from collection given index
    samples = list(self.collection["bin"].find(
        {   self.id: { 
                "$in": [ self.indices[_] for _ in batch] },
                "kind": { "$in": self.sample },             
        },  self.fields, )
    )

    # 2. Create a batch to store samples into
    results = []
    for id in batch:
        # 3. Fetch chunks from chunk indeces fetched in # 1.
        samples_for_id = [
            sample for sample in samples if sample[self.id] == self.indices[id]
        ]
        
        # 4. >>>> Recreate data from chunks <<<<
        data = self.make_serial(samples_for_id, self.sample[0])
        label = self.make_serial(samples_for_id, self.sample[1])

        data = self.normalize(self.transform(data).float())
        label = self.transform(label)

        results.append((data, label))
    return results
```

- Data integrity (so about them partial chunks)
- Batched reads 
- Data recreation

### 3. Swap
```
def swap(self, generated):
    """
    Moves data from write collection to read collection
    Deletes old write collection
    Maintains data integrity in between
    """
    time.sleep(2) # 0. Buffer for incomplete operations
    generated += self.swap_cap

    # 1. Rename the write collection to a temporary collection for processing
    self.db[self.collectionw].rename(self.collectiont, dropTarget=True)

    # 2. Reset the counter collection, push indeces are now at 0 and resumed
    self.reset_counter_and_collection()

    # 3. Remove excess chunks from the temporary collection
    result = self.db[self.collectiont].delete_many(
        {"id": { "$gt": self.swap_cap - 1 }})

    # 4. Go through collection, and reindex chunks into contiguous sections
    #       this operation is O(swap_cap)
    self.verify_collection_integrity(self.db[self.collectiont])

    # 5. Atomically replace read collection with temp collection
    self.db[self.collectiont].rename(self.collectionr, dropTarget=True)

    # 6. Flag the database as having swapped once and ready to be read
    self.db["status"].insert_one({"swapped": True})

    return generated 
```

- How swaps happen instantaneously
- How swaps happen safely
- How swap latency doesn't matter (push back latency) (maybe insert a cute figure here)

<br>

[^1]: for a typical image of shape 256x256x256, at 32 bits per voxel, that's 64 megabytes
[^2]: https://arxiv.org/abs/2107.09559
[^3]: see distributed computing
[^4]: see circular buffers
[^5]: see caches
[^6]: Note about how this is a complicated topic. Overfitting, mitigations by increasing generation throughput, etc.
[^7]: We tried python's multiprocessing library but found the gains not worth it in exchange for their added cost to complexity.
