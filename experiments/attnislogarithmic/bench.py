#!/usr/bin/env python3
import torch
import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Check if MPS is available (for macOS devices)
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS device")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"MPS not available, using {device}")

# Benchmark parameters
min_elements = 500
max_elements = int(1e6)
step_size = 500
warmup_runs = 10
benchmark_runs = 20

# Create lists to store results
element_counts = list(range(min_elements, max_elements + 1, step_size))
avg_times = []

# Progress bar for the entire benchmark
with tqdm(total=len(element_counts), desc="Benchmarking element counts") as pbar:
    
    # Loop through different element counts
    for num_elements in element_counts:
        times = []
        
        # Generate data
        a = torch.rand(num_elements, device=device)
        b = torch.rand(num_elements, device=device)
        
        # Warmup runs
        for _ in range(warmup_runs):
            # MPS sync before
            if device.type == "mps":
                torch.mps.synchronize()
            elif device.type == "cuda":
                torch.cuda.synchronize()
                
            _ = a * b
            
            # MPS sync after
            if device.type == "mps":
                torch.mps.synchronize()
            elif device.type == "cuda":
                torch.cuda.synchronize()
        
        # Actual benchmark runs
        for _ in range(benchmark_runs):
            # MPS sync before
            if device.type == "mps":
                torch.mps.synchronize()
            elif device.type == "cuda":
                torch.cuda.synchronize()
                
            start_time = time.time()
            _ = a * b
            
            # MPS sync after
            if device.type == "mps":
                torch.mps.synchronize()
            elif device.type == "cuda":
                torch.cuda.synchronize()
                
            end_time = time.time()
            times.append(end_time - start_time)
        
        # Calculate average time
        avg_time = sum(times) / len(times)
        avg_times.append(avg_time)
        
        # Update progress bar
        pbar.update(1)

# Prepare data for box plots - sample at regular intervals
sample_indices = list(range(0, len(element_counts), len(element_counts) // 10))
sample_element_counts = [element_counts[i] for i in sample_indices]

# Collect all timing data for box plots
boxplot_data = []
boxplot_labels = []

for idx in sample_indices:
    num_elements = element_counts[idx]
    # Generate data
    a = torch.rand(num_elements, device=device)
    b = torch.rand(num_elements, device=device)
    
    # Collect times for this element count
    times_for_boxplot = []
    for _ in range(benchmark_runs):
        # MPS sync before
        if device.type == "mps":
            torch.mps.synchronize()
        elif device.type == "cuda":
            torch.cuda.synchronize()
            
        start_time = time.time()
        _ = a * b
        
        # MPS sync after
        if device.type == "mps":
            torch.mps.synchronize()
        elif device.type == "cuda":
            torch.cuda.synchronize()
            
        end_time = time.time()
        times_for_boxplot.append((end_time - start_time) * 1000)  # Convert to ms for better visibility
    
    boxplot_data.append(times_for_boxplot)
    boxplot_labels.append(f"{num_elements}")

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
plt.style.use('dark_background')

# Line plot with axis lines on the first subplot
ax1.plot(element_counts, avg_times, '-', color='#50fa7b', linewidth=2)
ax1.scatter(element_counts[::10], avg_times[::10], color='#bd93f9', s=30)

ax1.set_title('Elementwise Multiplication Performance', fontname='.S NS Mono', fontsize=16)
ax1.set_xlabel('Number of Elements', fontname='.S NS Mono', fontsize=14)
ax1.set_ylabel('Average Time (seconds)', fontname='.S NS Mono', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(fontsize=12)

# Add axis lines
ax1.axhline(y=0, color='white', linestyle='-', alpha=0.3)
ax1.axvline(x=0, color='white', linestyle='-', alpha=0.3)
ax1.spines['bottom'].set_visible(True)
ax1.spines['left'].set_visible(True)
ax1.spines['top'].set_visible(True)
ax1.spines['right'].set_visible(True)
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['right'].set_color('white')

# Box plot on the second subplot
bp = ax2.boxplot(boxplot_data, patch_artist=True, labels=boxplot_labels)

# Style the box plot
for box in bp['boxes']:
    box.set(facecolor='#50fa7b', alpha=0.6)
for whisker in bp['whiskers']:
    whisker.set(color='#bd93f9', linewidth=1.5)
for cap in bp['caps']:
    cap.set(color='#bd93f9', linewidth=1.5)
for median in bp['medians']:
    median.set(color='#ff79c6', linewidth=2)
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='#ff5555', markersize=5)

ax2.set_title('Time Distribution by Element Count', fontname='.S NS Mono', fontsize=16)
ax2.set_xlabel('Number of Elements', fontname='.S NS Mono', fontsize=14)
ax2.set_ylabel('Time (milliseconds)', fontname='.S NS Mono', fontsize=14)
ax2.grid(True, linestyle='--', alpha=0.7)

# Rotate x-axis labels for better readability
ax2.set_xticklabels(boxplot_labels, rotation=45, fontname='.S NS Mono')

# Add axis lines
ax2.axhline(y=0, color='white', linestyle='-', alpha=0.3)
ax2.axvline(x=0, color='white', linestyle='-', alpha=0.3)
ax2.spines['bottom'].set_visible(True)
ax2.spines['left'].set_visible(True)
ax2.spines['top'].set_visible(True)
ax2.spines['right'].set_visible(True)
ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')
ax2.spines['top'].set_color('white')
ax2.spines['right'].set_color('white')

plt.tight_layout()

# Save the plot
plt.savefig('elementwise_benchmark.png', dpi=300, bbox_inches='tight')

# Print results summary
print("\nBenchmark Results:")
print(f"Device: {device}")
print(f"Element count range: {min_elements} to {max_elements}")
print(f"Average time for {min_elements} elements: {avg_times[0]:.6f} seconds")
print(f"Average time for {max_elements} elements: {avg_times[-1]:.6f} seconds")
print(f"Plot saved as 'elementwise_benchmark.png'")

plt.show()
