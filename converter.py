from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from math import floor
import os

import extracter

def split_text_into_lines(text, max_chars_per_line):
    # Split text into words
    words = text.split()
    
    lines = []
    current_line = []
    current_length = 0
    
    # Add words to the current line until it exceeds the maximum number of characters
    for word in words:
        if current_length + len(word) + 1 <= max_chars_per_line:
            current_line.append(word)
            current_length += len(word) + 1  # +1 accounts for the space
        else:
            # Join the current line into a string and add to lines
            lines.append(' '.join(current_line))
            # Start a new line with the current word
            current_line = [word]
            current_length = len(word)
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_bionic_pdf(output_path, text):
    # Create a PDF canvas
    c = canvas.Canvas(output_path, pagesize=letter)

    # Set the font to Helvetica-Bold with a font size of 12
    c.setFont("Helvetica-Bold", 12)
    x = 60
    x_start = x
    y = 750  # Starting Y position (top of the page)
    font_size = 12
    max_chars_per_line = 90

    # Split text into lines for proper placement
    # lines = text.split('\n')
    lines = split_text_into_lines(text, max_chars_per_line)


    # Loop through each line and add it to the PDF
    for line in lines:
        words = line.split(' ')
        if y < 50:  # If we're near the bottom of the page, create a new page
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            y = 750  # Reset Y position for the new page
        
        for word in words:
            l = len(word)
            mid = floor(l / 2)
            if l % 2 == 0:
                mid += 1
            bionic_part = word[: mid]
            orig_part = word[mid :]
            # Set font to bold for the first half
            c.setFont("Helvetica-Bold", font_size)
            c.drawString(x, y, bionic_part)
            
            # Calculate the width of the bold part to properly position the non-bold part
            bold_width = c.stringWidth(bionic_part, "Helvetica-Bold", font_size)
            
            # Set font to regular for the second half
            c.setFont("Helvetica", font_size)
            c.drawString(x + bold_width, y, orig_part)
            
            # Move x for the next word (add space after the word)
            word_width = c.stringWidth(word, "Helvetica", font_size)
            # x += word_width + c.stringWidth(' ', "Helvetica", font_size)  # Adjust spacing between words    
            x += word_width + 5

        # update x and y
        x = x_start
        y -= 20
    # Save the PDF
    c.save()

def main():
    files = os.listdir('./orig')
    for file in files:
        orig_path = './orig/' + file
        output_path = './bionic/bionic_' + file
        text = extracter.extract_text_from_pdf(orig_path)
        create_bionic_pdf(output_path, text)
        
        # Call the function to create the half-bold text PDF
        print(f"PDF '{output_path}' has been created successfully.")

if __name__ == "__main__":
    main()