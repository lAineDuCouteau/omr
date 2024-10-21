# import cv2
# import numpy as np

# def omr_processing(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     # Resize image if needed
#     image = cv2.resize(image, (800, 1000))  # Adjust size as per your sheet
    
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply binary threshold to make the paper white and answers black
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

#     # Define the grid positions for the answer bubbles


#     # Draw rectangles around bubble positions
#     for question, bubbles in answer_bubbles.items():
#         for i, (x, y) in enumerate(bubbles):
#             cv2.rectangle(image, (x-20, y-20), (x+20, y+20), (0, 0, 255), 2)  # Red rectangle for each bubble
    
#     # Save the debug image with marked areas
#     cv2.imwrite('bubble_positions.png', image)
    
#     return 'Check bubble_positions.png for bubble alignment'

import cv2
import numpy as np

def omr_processing(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Resize image if needed (adjust size based on the sheet size)
    image = cv2.resize(image, (800, 1000))  # Adjust size as per your sheet
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold to make the paper white and answers black
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Define the grid positions for the answer bubbles
    # Adjust these coordinates according to the actual bubble locations on the image
    answer_bubbles = {
        1: [(171, 535), (311, 535), (451, 535), (601, 535)],  # Q1: A, B, C, D positions
        2: [(171, 601), (311, 601), (451, 601), (601, 601)],  # Q2: A, B, C, D positions
        3: [(171, 671), (311, 671), (451, 671), (601, 671)],  # Q3: A, B, C, D positions
        4: [(171, 740), (311, 740), (451, 740), (601, 740)],  # Q4: A, B, C, D positions
        5: [(171, 809), (311, 809), (451, 809), (601, 809)],  # Q5: A, B, C, D positions
    }
    
    answer_key = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'C'}  # Define the correct answers
    
    marked_answers = {}
    
    # Visualize detection for debugging
    for question, bubbles in answer_bubbles.items():
        for i, (x, y) in enumerate(bubbles):
            # Draw rectangles on the image to visualize bubble positions
            cv2.rectangle(image, (x-20, y-20), (x+20, y+20), (255, 0, 0), 2)  # Blue rectangle for each bubble
            
            # Extract region of interest (ROI) for each bubble
            roi = thresh[y-20:y+20, x-20:x+20]  # Small region around the bubble
            
            # Check if the ROI is filled (marked)
            filled = cv2.countNonZero(roi)
            if filled > 500:  # Threshold for considering it marked
                marked_answers[question] = chr(65 + i)  # 'A' is 65 in ASCII, 'B' is 66, etc.
                cv2.putText(image, "Marked", (x - 40, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                break  # Stop once we've found the marked bubble for this question
    
    # Calculate the score
    correct_answers = 0
    for question, marked in marked_answers.items():
        if marked == answer_key[question]:
            correct_answers += 1
    
    # Save the debug image with marked areas for checking
    cv2.imwrite('marked_answer_sheet.png', image)
    
    return correct_answers
