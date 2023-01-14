import json
import tinytuya
from flask import Flask, abort, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

lightBulb = tinytuya.OutletDevice('bf6fe6278bc779da94d49v', '192.168.18.8', 'a5e0fef167323362', version=3.4)
windowRight = tinytuya.CoverDevice('bf1bcf4ed0e156e13bsbvz', '192.168.18.6', 'c6db31d029839f98', version=3.3)
windowLeft = tinytuya.CoverDevice('bf013c91d887adce65taat', '192.168.18.7', '651823889d72de81', version=3.3)

if __name__ == '__main__':
    app.run()


@app.route('/')
def dashboard():
    return render_template('index.html')


# Light requests
@app.route('/light/set/<int:status>')
def light_set(status):
    if status == 1:
        lightBulb.turn_on()
        return json.dumps({
            'success': True,
            'message': 'Light on'
        })
    elif status == 0:
        lightBulb.turn_off()
        return json.dumps({
            'success': True,
            'message': 'Light off'
        })
    else:
        return json.dumps({
            'success': False,
            'message': 'Invalid status '
        })


@app.route('/light/status')
def light_status():
    data = lightBulb.status()
    return json.dumps({'success': True, 'status': data['dps']['1']})


# Window requests
@app.route('/window/set/<side>/<int:data>')
def window_set(side=None, data=None):
    side = get_side(side)
    if not side:
        return json.dumps({'success': False, 'message': 'Invalid window.'})

    if data == 0:
        side.send(side.generate_payload(tinytuya.CONTROL, {"1": "stop"}))
        return json.dumps({
            'success': True,
            'message': 'Stopping window'
        })
    elif data == 1:
        side.send(side.generate_payload(tinytuya.CONTROL, {"1": "open"}))
        return json.dumps({
            'success': True,
            'message': 'Opening window'
        })
    elif data == 2:
        side.send(side.generate_payload(tinytuya.CONTROL, {"1": "close"}))
        return json.dumps({
            'success': True,
            'message': 'Closing window'
        })
    else:
        return json.dumps({
            'success': False,
            'message': 'Invalid status'
        })


@app.route('/window/status/<side>')
def window_status(side):
    side = get_side(side)
    if not side:
        return json.dumps({'success': False, 'message': 'Invalid window.'})

    data = side.status()
    return json.dumps({
        'success': True,
        'status': data['dps']['1'],
        'value': data['dps']['2'],
    })


@app.route('/status')
def all_devices_status():
    lightData = lightBulb.status()['dps']['1']
    windowLeftData = windowLeft.status()['dps']
    windowRightData = windowRight.status()['dps']

    if windowLeftData['1'] == 'stop':
        windowLeftData = windowLeftData['2']
    else:
        windowLeftData = windowLeftData['1']

    if windowRightData['1'] == 'stop':
        windowRightData = windowRightData['2']
    else:
        windowRightData = windowRightData['1']

    return json.dumps({
        'success': True,
        'data': {
            'light': lightData,
            'windowLeft': windowLeftData,
            'windowRight': windowRightData,
        }
    })


def get_side(data):
    if data == 'left':
        return windowLeft
    elif data == 'right':
        return windowRight
    else:
        return False
