from flask import Flask, render_template, request, redirect, url_for, session
import os
import time
import cv2

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/', methods=['GET'])
def index():
    return render_template('initialScreen.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('initialScreen.html')

@app.route('/home', methods=['POST'])
@app.route('/', methods=['POST'])
def submit():
    # Get the user's name from the submitted form
    name = request.form['name']
    session['name'] = name

    # Generate a filename using the user's name
    filename = name.lower().replace(' ', '_') + '.jpg'

    # # Take a photo using the computer's camera using a command-line tool such as 'imagesnap'
    # os.system('imagesnap ./images/{}'.format(filename))
    capture_image("./static/images/" + filename)

    # Wait for 1 second to ensure that the photo is saved before redirecting
    time.sleep(1)

    # Redirect to the page that displays the list of images
    return redirect(url_for('images', name=name))

@app.route('/images/<name>')
def images(name):
    # Get a list of all image files in the "images" folder
    images = get_images()

    # # Set the idle timeout to 10 seconds
    # session['last_activity'] = time.time()

    # Render the "images.html" template with the list of images and associated names
    return render_template('images.html', name=name, images=images)

# @app.before_request
# def before_request():
#     # Check if the user is idle for more than 10 seconds
#     if 'last_activity' in session and time.time() - session['last_activity'] > 10:
#         session.pop('last_activity', None)
#         return redirect(url_for('index'))

# @app.route('/bid', methods=['POST'])
# def bid():
#     # Handle the bid form submission
#     bid_amount = request.form['bid']
#     filename = request.form['filename']
#     # Update the bid for the image with the given filename
#     # (you'll need to implement this part yourself)
#     return redirect(request.referrer)

@app.route('/bid/<image_name>/<bidder_name>', methods=['GET', 'POST'])
def bid(image_name, bidder_name):
    if request.method == 'POST':
        bid_value = int(request.form['bid'])
        current_highest_bid = session.get(f'{image_name}_highest_bid', 0)
        current_highest_bidder = session.get(f'{image_name}_highest_bidder', '')
        images = get_images()

        if bid_value > current_highest_bid:
            session[f'{image_name}_highest_bid'] = bid_value
            session[f'{image_name}_highest_bidder'] = bidder_name

        return redirect(url_for('images', name=bidder_name, images=images))
    filename_parts = image_name.lower().split()  # convert to lowercase and split into parts
    filename = "_".join(filename_parts) 
    return render_template('bid.html', name=bidder_name, image_name=image_name, filename=filename)

def get_images():
    images = []
    for img in os.listdir('./static/images'):
        img_name = img.split('.')[0].replace('_', ' ').title()
        images.append({'filename': img, 'name': img_name})
    return images

def capture_image(filename):
    cap = cv2.VideoCapture(0)  # use default camera (0)
    ret, frame = cap.read()
    for _ in range(5):
        ret, frame = cap.read()  # read a frame from the camera
    if ret:
        cv2.imwrite(filename, frame)  # save the frame as an image file
    cap.release()  # release the camera

if __name__ == '__main__':
    app.run(debug=True)
