import tkinter as tk
import sys
from rectpack import newPacker

# CustomCanvas: Wrapper around Tkinter Canvas
class CustomCanvas:
    def __init__(self, height: int, width: int):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=height, width=width)
        self.canvas.pack()

    def draw_rectangle(self, x, y, width, height, color="blue"):
        """Draws a rectangle on the canvas."""
        self.canvas.create_rectangle(x, y, x + width, y + height, outline="black", fill=color)

    def display(self):
        """Displays the canvas and starts the Tkinter event loop."""
        self.root.mainloop()

# Rectangle Class
class Rectangle:
    def __init__(self, height: int, width: int, x: int = 0, y: int = 0):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Rectangle({self.width}x{self.height} at ({self.x}, {self.y}))"

# Pack function using rectpack
def pack(allRect, canvasSize):
    """Packs rectangles without overlap using rectpack."""
    packer = newPacker()

    # Add rectangles to packer
    for rect in allRect:
        packer.add_rect(rect.width, rect.height)

    # Add one bin (canvas) with max width/height
    packer.add_bin(canvasSize[1], canvasSize[0])

    # Run the packing algorithm
    packer.pack()

    packed_rectangles = []
    
    # Extract packed positions
    for bin in packer:
        for rect in bin:
            x, y, w, h = rect
            packed_rectangles.append(Rectangle(h, w, x, y))  # Keep width and height order

    return packed_rectangles

# Main Function
def main():
    """Reads input, processes rectangles, and displays them if running locally."""
    if len(sys.argv) < 2:
        print("Usage: python Assignment5.py <input_file>")
        return

    filename = sys.argv[1]

    # Read and validate input file
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines or len(lines) < 2:
            raise ValueError("Error: Input file must contain at least one rectangle and a valid canvas size.")

        # Read canvas size
        canvasSize = tuple(map(int, lines[0].split(",")))

        # Read rectangles
        allRect = []
        for line in lines[1:]:
            try:
                height, width = map(int, line.split(","))
                allRect.append(Rectangle(height, width))
            except ValueError:
                print(f"Warning: Skipping malformed line -> {line}")

    except Exception as e:
        print(f"Error: {e}")
        return

    # Pack rectangles
    packedRects = pack(allRect, canvasSize)

    # Display graphics only when running locally
    if __name__ == "__main__":
        canvas = CustomCanvas(canvasSize[0], canvasSize[1])
        colors = ["red", "green", "blue", "yellow", "purple", "orange"]

        for i, rect in enumerate(packedRects):
            canvas.draw_rectangle(rect.x, rect.y, rect.width, rect.height, colors[i % len(colors)])

        canvas.display()

# Entry Point
if __name__ == "__main__":
    main()
