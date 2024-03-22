> [!quote]plurality should not be posited without necessity

When learning new things, I've found it extremely helpful to explain things in their simplest forms.

This page includes my explainations of some of the tougher ideas I've come across. I'll append more as more difficult concepts crop up.

# Reverse Mode Automatic differentiation #

[Automatic Differentiation](https://en.wikipedia.org/wiki/Automatic_differentiation)(AD) is a way to calculate the rate of change of outputs of computer programs with respect to their inputs. There are two forms of AD: forward mode, which efficientily calculates the rate of change of all outputs with respect to some input, and reverse mode (also known as backpropagation), which efficiently calculates the rate of change of one output with respect to all of its inputs.

You need three things to perform reverse mode automatic differentitation:
1. Functions that you know how to differentitate.
2. A way to hook up functions together, such the functions always go from input to output, and never the other way around, creating a flow chart.
3. The Chain Rule from calculus, which essentially says "when functions are nested, their rates of change multiply"

Using these components, you can differentiate anything that is composable using those atomic functions. You do this by first expressing your program using these atomic functions (such as a simple neural network by using matrix multiplications). You then culminate this program into a single output (such as a loss function. Then to calculate the rate of change of the output (the loss function) with respect to all its inputs (the neural network matrix weights), you calculate the rate of change of all computations, and multiply them together using chain rule in the reverse order of your flow chart.
