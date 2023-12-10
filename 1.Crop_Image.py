import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded image to the uploads folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.png')
        file.save(filename)

        # Load and process the image
        image = cv2.imread(filename)
        
        # Split the image and save the parts as you did before
        # Get the dimensions of the image
        height, width, _ = image.shape

        # Calculate the width of each part
        part_width = width // 3

        # Split the image into three parts
        part1 = image[:, 0:part_width]
        part2 = image[:, part_width:2*part_width]
        part3 = image[:, 2*part_width:3*part_width]

        # Save or process the three parts as needed
        cv2.imwrite('Split Images\Part1.png', part1)
        cv2.imwrite('Split Images\Part2.png', part2)
        cv2.imwrite('Split Images\Part3.png', part3)
        print("crop completed")
        
        # Run the second script to process the parts
        subprocess.run(["python", "2.Pre-Processing.py"])

        return redirect(url_for('processed_image'))


        #result = subprocess.check_output(["python", "2.Pre-Processing.py"], universal_newlines=True)
        #return render_template('result.html', result=result)


@app.route('/processed_image')
def processed_image():
    #processed_image_path = '11.Segmented_Image.jpg'
    #return send_from_directory('.', '11.Segmented_Image.jpg')


    predictions_file_path = '14.predictions.txt'
    
    # Read the content of predictions.txt
    with open(predictions_file_path, 'r', encoding='utf-8') as predictions_file:
        predictions_content = predictions_file.read()

    # Render the result along with the image on the same page
    return render_template('result.html', predictions=predictions_content)

@app.route('/processed_image_file')
def processed_image_file():
    processed_image_path = '11.Segmented_Image.jpg'
    return send_from_directory('.', '11.Segmented_Image.jpg')




if __name__ == '__main__':
    app.run(debug=True)
