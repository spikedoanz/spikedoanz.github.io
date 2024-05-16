# wirehead, a data pipeline for ml on synthetic data # 

<img src="https://github.com/spikedoanz/spikedoanz.github.io/blob/master/assets/wirehead.png?raw=true" alt="Wirehead Image">

## the problem 

- want synthetic data
- synthetic data massive (say, 256^3 * channels massive) and you don't have a crazy hard drive

## the solution 

introducing wirehead, an overengineered data pipeline, bootstrapped off of mongodb. it allows you to:

- infinitely scale synthetic data generating jobs (decoupled writes)
- **not** scale synthetic data generating jobs to match training job throughput (decoupled reads)
- be incredibly fast (all in memory, using infiniband)

[code](https://github.com/neuroneural/wirehead)

[technical report](coming soon)

## high level ##

### ideas ###

wirehead is the combination of the following three ideas:

- decoupled read and write halves: semaphore? I barely even know her! concurrent programming is hard, especially with distributed systems that don't behave nicely -> get rid of the problem entirely
- decoupled throughput: data is generated on the fly, but reads and writes happen at different speeds -> use circular queues to allow reads to happen as fast as they want
- smart swaps: the databases store up to 500 gigs at any given time -> don't move that, silly. instead, move the database identifiers (in mongodb, these are called 'collection names')

### components ###

wirehead contains the following three components: 
- generators (aka writers): these are just your data generators with a wrapper to make them push to mongodb. more on technical challenges of doing this at lower level
- dataloader (aka reader, aka training job): a fancy  torch dataloader that implements a circular queue implicitly by using modular arithmetic, has somewhat robust error handling.
- manager: monitors, swaps, and indexes databases. 

at runtime, training jobs are usually run on dedicated training nodes, however manager and generators can be combined due to the low overhead of managing the database.

### control flow ###

1. fire up generators (right now only supports slurm), each gets assigned a unique id based on slurm job queues. whatever job gets spawned first automatically becomes the manager.
2. generators start filling up the write collection, out of order, with chunked data 
3. once the write half becomes full, mananger kicks in, moves the write half to a temp collection(by only changing its identifier), reindexes (because all the writes were happening out of order, and also the data is chunked), then moves it to the read collection 
4. the training job waiting on the other side kicks in and starts reading
5. once write becomes full again, jump to step 3

## low level ##

if you're interested enough to read to this point in the article, and think this kind of engineeering is something you need, consider reaching out. i'm an engineer without a permanent home (grad school) at the moment, and would love to colaborate.


### challenges ###
- tensors can be massive. for the neuroimaging tasks we have, it's 256^3 (spatial) * n (channels). assuming the smallest, single channel, uint8 tensors, it's still 16MiB per sample. 
- mongodb has a [document size cap](https://www.mongodb.com/docs/v5.2/reference/limits/) of 16 megabytes. that means we have to chunk it.
``` 
def chunk_binobj(tensor_compressed, id, kind, chunksize):
            """ Convert chunksize from megabytes to bytes """
            chunksize_bytes = chunksize * 1024 * 1024

            # Calculate the number of chunks
            num_chunks = len(tensor_compressed) // chunksize_bytes
            if len(tensor_compressed) % chunksize_bytes != 0:
                num_chunks += 1

            # Yield chunks
            for i in range(num_chunks):
                start = i * chunksize_bytes
                end = min((i + 1) * chunksize_bytes, len(tensor_compressed))
                chunk = tensor_compressed[start:end]
                yield {
                    "id": id,
                    "chunk_id": i,
                    "kind": kind,
                    "chunk": bson.Binary(chunk),
                }
```
- documents are pushed out of order, but have to be reassembled in order at read time. this can be solved by giving each chunk a secondary id (in this case, 'index')
```
def generate_and_insert(self,
						collection_bin,
						counter_collection,
						chunk_size):
	""" Fetch from generator and inserts into mongodb """
	# 0. Fetch data from generator
	data = next(self.generator)
	# 1. Get the correct index for this current sample
	index = self.get_current_idx(counter_collection)
	# 2. Turn the data into a list of serialized chunks  
	chunks = self.chunkify(data, index, chunk_size)
	# 3. Push to mongodb + error handling
	self.push_chunks(collection_bin, chunks)
```

### considerations ###

1. **why not redis?**

the first prototype of wirehead actually did use redis, and was much simpler. however redis is single threaded, and this was a major bottleneck once training jobs with crazy reads/second got introduced.

2. **what's the catch?**

the catch is that to store N bytes of data at any given time, 2N room must be given in memory for the read and write halves. this isn't really a tradeoff though, as reducing N gives you a more frequent refreshes and samples. 

furthermore, considering that Ns too large might make the training job unable to use the read the database before a swap, this tradeoff is rendered somewhat moot.

in testing, i've been using N of anywhere from 1,000 to 10,000, with barely any noticable difference.

3. **what's the future of this project?**

right now, wirehead is gaining its first couple of rounds of users (besides me) all of these people are at my lab, also using slurm, so there isn't really a reason to switch just yet. that said, do reach out if you want support for platforms that aren't slurm.

---

## notes ##

this article is a wip blog version of the technical report for a paper. expect many edits.

last edit: 2024-05-16
