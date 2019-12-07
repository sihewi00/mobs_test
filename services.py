from flask import Flask
from flask import request
from flask import jsonify
from sense_hat import SenseHat
from random import randint
from flask_cors import CORS

app = Flask(__name__)

# Disable CORS protection altogether
cors = CORS(app, resources={
            r"/status": {"origins": "*"}, r"/music": {"origins": "*"}, r"/action/*": {"origins": "*"}})

# Allow only specific IP for CORS
# cors = CORS(app, resources={r"/status": {"origins": "http://192.168.0.204"}, r"/action/*": {"origins": "http://192.168.0.204"}})


@app.route('/status')
def status():

    sense = SenseHat()

    consumption = 3 + randint(0, 100) / 20

    f = open("speed.txt", "r")
    speed = int(f.read())

    speed = speed + randint(-12, 12)

    if speed > 185:
        speed = 185

    if speed < 0:
        speed = 0

    f = open("speed.txt", "w")
    f.write(str(speed))
    f.close()

    return jsonify(
        pressure=sense.get_pressure(),
        temp=sense.get_temperature(),
        humidity=sense.get_humidity(),
        consumption=consumption,
        speed=speed
    )


@app.route('/music')
def music():

    music = [{
        'title': 'Shout',
        'artist': 'Tears for Fears',
        'path': 'music/Tears_for_Fears_-_Shout.mp3'
    },
    {
        'title': 'Our Darkness',
        'artist': 'Anne Clark',
        'path': 'music/Anna_Clark_-_Our_Darkness.mp3'
    },
	{
        'title': 'Fade to Grey',
        'artist': 'Visage',
        'path': 'music/Visage_-_Fade_to_Grey.mp3'
    }]

    return jsonify(music)


@app.route('/action/<action>')
def action(action):

    sense = SenseHat()
    sense.show_message(request.remote_addr, text_colour=(
        255, 255, 0), back_colour=(127, 0, 127))

    if action == "lock":

        b = (0, 0, 0)
        r = (255, 0, 0)

        pixels = [
            b, b, b, b, b, b, b, b,
            b, b, b, r, r, b, b, b,
            b, b, r, b, b, r, b, b,
            b, b, r, b, b, r, b, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b
        ]

    elif action == "unlock":

        b = (0, 0, 0)
        r = (0, 255, 0)

        pixels = [
            b, b, b, b, b, r, r, b,
            b, b, b, b, r, b, b, r,
            b, b, b, b, b, b, b, r,
            b, b, b, b, b, b, r, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b,
            b, b, r, r, r, r, b, b
        ]

    sense.set_pixels(pixels)

    return jsonify(
        status=0
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
