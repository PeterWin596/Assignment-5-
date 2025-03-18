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
from rectpack import newPacker

def pack(allRect, canvasSize):
    """Packs rectangles without overlapping and ensures all fit within bounds."""
    packer = newPacker(rotation=False)  # Disable rotation to match expected behavior

    # Dictionary to track original Rectangle objects
    rect_map = {}

    # Add rectangles to packer and store their ID
    for i, rect in enumerate(allRect):
        packer.add_rect(rect.width, rect.height, rid=i)  # Assign ID
        rect_map[i] = rect  # Store original Rectangle object with ID

    # Add a slightly larger bin to improve packing efficiency
    bin_width = canvasSize[1] + 10  # Small buffer
    bin_height = canvasSize[0] + 10  # Small buffer
    packer.add_bin(bin_width, bin_height)  

    # Run the packing algorithm
    packer.pack()

    packed_rectangles = []

    # Extract packed positions
    for abin in packer:
        for rect in abin:
            x, y, w, h = rect.x, rect.y, rect.width, rect.height  # Ensure correct values
            rect_id = rect.rid  # Get the rectangle ID
            original_rect = rect_map[rect_id]  # Retrieve original Rectangle object

            # Clamp positions to stay within canvas bounds
            x = min(max(0, x), canvasSize[1] - w)
            y = min(max(0, y), canvasSize[0] - h)

            # Ensure we return a Rectangle object
            packed_rectangles.append(Rectangle(original_rect.height, original_rect.width, int(x), int(y)))

    # Verify all rectangles were packed
    if len(packed_rectangles) != len(allRect):
        print(f"Warning: Expected {len(allRect)} rectangles but only packed {len(packed_rectangles)}.")

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
