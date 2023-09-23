Unless if you are somehow living under a rock for the past year, you probably have heard of [chatGPT](https://chat.openai.com/). It can write code, solve logic puzzles, write essays. You can even talk to it! If not for the ever present reminders of "As an AI language model...", you'd be forgiven for thinking that it was a person on the other side sometimes.
![[Pasted image 20230922185604.png]]
And yet, it's an surprisingly simple machine! If [semianalysis](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure) is to be believed, GPT 4 is simply a scaled up and ensembled version of GPT 3.5, which in itself is a scaled up version of GPT 2. Taking a look at its [repo](https://github.com/openai/gpt-2/blob/master/src/model.py) from OpenAI reveals that for inference, the code is not even 200 lines long. Jay Mody has an excellent article where he managed to cut it down to [60 lines of code](https://jaykmody.com/blog/gpt-from-scratch/)! That article covers all of the relevant technical details, and along with Kaparthy's wonderful [tutorial](https://www.youtube.com/watch?v=kCc8FmEb1nY) and an adorable pure C [implementation](https://github.com/karpathy/llama2.c) of Facebook's LLaMa model, served as the main inspirations and resources for my own project. 

Instead, this article will be focused on some of the broader lessons I learnt after doing my own toy implimentation of GPT 2, plus experience after doing work with LLMs for the past few months.

1. No one knows what's going on

The code tells you almost nothing about the model behavior.
The specific effects of using softmax instead of relu, or different configurations attention heads or whatever have very little to do with how the model behaves in practice.
Current methods of understanding LLMs are more Pavlov than they are Einstein. The "model" is known, but "studying" looks very behavioral.

2. Optimizers are terrifying and beautiful

No one hand coded GPT's behaviors
Encoded inside of GPT's paramters are something akin to the function for human langauge
Natural selection is one of these, and MuZero is a good terrifying parallel.
In the specific case of GPT however, we probably don't have to worry too much. (binary cross entropy only gets you TO human capabilities, not past)
Until some crazy hacks happen (maybe with some huge lessons in curating synthetic data), the only thing that GPT will have an impact on, is the cost of median human output.

3. Every human craft is probably going to change.

I extensively used GPT 4 to help me with the concepts and some of the code snippets inside my own implementation. This project would've probably taken a whole week otherwise.

My workflow has been completely changed to incorporate GPT as a form of pair programming

Problems that were NP that are now essentially O(1):
- Not knowing convention 
- Not knowing how code worked
- Having someone more knowledgeable explain things to me
- Being able to verify my understanding by explaining things back
- Understanding math jargon
- Overcoming the self imposed barrier of understanding

I've been applying the same thing to a whole host of other things: studying language, getting back into writing, etc