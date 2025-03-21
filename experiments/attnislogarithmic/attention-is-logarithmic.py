from prettytable import PrettyTable


print("Unary (*)")
table = PrettyTable()
# Configure the table appearance
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]

# Add rows
table.add_row(["", "", "", ""])
table.add_row(["LOAD", "1", "[a_1 a_2 ... a_i]", "n"])
table.add_row(["LOAD", "1", "[b_1 b_2 ... b_i]", "n"])
table.add_row(["MUL", "1", "*  *      *", "n"])
table.add_row(["STORE", "1", "[c_1 c_2 ... c_i]", "n"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "4", "", "4n"])
table.add_row(["ASYMP", "O(1)", "", "O(n)"])

print(table)




# Create the table
table = PrettyTable()
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]


print("Sum")

# Add the data rows
table.add_row(["LOAD", "1", "[a_1     a_2     a_3     a_4  ⋯  a_i]", "n/2"])
table.add_row(["", "", " \\     /       \\     /       /", ""])
table.add_row(["PAIRWISE +", "1", " [a_1+a_2         a_3+a_4   ⋯  ]", "n/4"])
table.add_row(["", "", "    \\           /        /", ""])
table.add_row(["PAIRWISE +", "1", "    [(a_1+a_2)+(a_3+a_4) ⋯ ]", "n/8"])
table.add_row(["", "", "      \\   /", ""])
table.add_row(["⋯", "⋯",            "      ⋯", "⋯"])
table.add_row(["", "",              "      |", ""])
table.add_row(["PAIRWISE +","1",    "     [∑a]", "1"])
table.add_row(["STORE", "1",        "     [∑a]", "1"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "(logn)+1", "", "n+1"])
table.add_row(["", "", "", ""])
table.add_row(["ASYMP", "O(log n)", "", "O(n)"])

# Adjust column widths to match the ASCII art version
table.min_width["op"] = 12
table.min_width["depth"] = 9
table.min_width["input"] = 35
table.min_width["work"] = 12

# Print the table
print(table)

print("Tensor")

# Create the matrix multiplication table
table = PrettyTable()
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]
# Add rows with empty row for spacing
table.add_row(["", "", "", ""])
table.add_row(["LOAD", "1", "[a_11 a_12 ⋯ a_1j ⋯ a_ij]", "n²"])
table.add_row(["LOAD", "1", "[b_11 b_12 ⋯ b_1k ⋯ b_jk]", "n²"])
table.add_row(["MUL", "1", "*   *     *     *", "n³"])
table.add_row(["STORE", "1", "[c_111 c_112 ⋯ c_1jk ⋯ c_ijk]", "n³"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "4", "", "2n²+2n³"])
table.add_row(["", "", "", ""])
table.add_row(["ASYMP", "O(1)", "", "O(n³)"])
print(table)


print("Matmul")

# Create the tensor operations table
table = PrettyTable()
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]

# Add rows with empty rows for spacing
table.add_row(["", "", "", ""])
table.add_row(["LOAD", "1", "[a_11 a_12 ⋯ a_1j ⋯ a_ij]", "n²"])
table.add_row(["LOAD", "1", "[b_11 b_12 ⋯ b_1k ⋯ b_jk]", "n²"])
table.add_row(["TENSOR", "1", "\"ij,jk->ijk\"", "n³"])
table.add_row(["CONTRACT", "log n", "\"ijk->ik\"", "n³"])
table.add_row(["STORE", "1", "[d_11 d_12 ⋯ d_1k ⋯ d_ik]", "n²"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "(logn)+4", "", "2n²+2n³"])
table.add_row(["", "", "", ""])
table.add_row(["ASYMP", "O(log n)", "", "O(n³)"])
print(table)


# Create the softmax table
table = PrettyTable()
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]

# Add rows for softmax
table.add_row(["LOAD", "1", "x ∈ ℝⁿ", "n"])
table.add_row(["MAX", "log n", "m = max(x)", "n"])
table.add_row(["SUB", "1", "x' = x - m", "n"])
table.add_row(["EXP", "1", "e = exp(x')", "n"])
table.add_row(["SUM", "log n", "s = sum(e)", "n"])
table.add_row(["DIV", "1", "y = e / s", "n"])
table.add_row(["STORE", "1", "y ∈ ℝⁿ", "n"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "2log n+5", "", "7n"])
table.add_row(["", "", "", ""])
table.add_row(["ASYMP", "O(log n)", "", "O(n)"])

# Set minimum column widths for softmax table
table.min_width["op"] = 14
table.min_width["depth"] = 11
table.min_width["input"] = 32
table.min_width["work"] = 8

print("Softmax Operations Table:")
print(table)
print("\n")

# Create the attention mechanism table
table = PrettyTable()
table.header = True
table.border = True
table.field_names = ["OP", "DEPTH", "INPUT", "WORK"]

# Add rows for attention mechanism
table.add_row(["LOAD", "1", "X ∈ ℝᵇˣⁿˣᵈ", "bnd"])
table.add_row(["LOAD", "1", "Wq,Wk,Wv ∈ ℝᵈˣᵈ", "3d²"])
table.add_row(["MATMUL", "3log d", "Q = X·Wq ; K = X·Wk ; V = X·Wv", "3bnd²"])
table.add_row(["MATMUL", "log d", "S = Q·Kᵀ", "bn²d"])
table.add_row(["DIV", "1", "S' = S / √d", "bn²"])
table.add_row(["SOFTMAX", "log n", "A = softmax(S')", "bn²"])
table.add_row(["MATMUL", "log n", "O = A·V", "bn²d"])
table.add_row(["STORE", "1", "O ∈ ℝᵇˣⁿˣᵈ", "bnd"])
table.add_row(["", "", "", ""])
table.add_row(["TOTAL", "4log d +\n2log n + 5", "", "≈ bn²d"])
table.add_row(["", "", "", ""])
table.add_row(["ASYMP", "O(logd)\nif d >>n", "", "O(bn²d)"])

# Set minimum column widths for attention table
table.min_width["op"] = 14
table.min_width["depth"] = 11
table.min_width["input"] = 32
table.min_width["work"] = 11

print("Attention Mechanism Operations Table:")
print(table)
