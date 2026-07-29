# Method 1: Extract letter at a specific index
text = "Hello World"
index = 0
letter = text[index]
print(letter)  # Output: H

# Method 2: Extract multiple specific letters by index
text = "Hello World"
indices = [0, 1, 6]
letters = [text[i] for i in indices]
print(letters)  # Output: ['H', 'e', 'W']

# Method 3: Extract all occurrences of a specific letter
text = "Hello World"
target_letter = "l"
occurrences = [i for i, letter in enumerate(text) if letter == target_letter]
print(occurrences)  # Output: [2, 3, 9]

# Method 4: Extract first occurrence of a specific letter
text = "Hello World"
target_letter = "o"
position = text.find(target_letter)
print(position)  # Output: 4