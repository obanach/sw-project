import json
import tinytuya
from flask import Flask, abort

app = Flask(__name__)
lightBulb = tinytuya.OutletDevice('bf6fe6278bc779da94d49v', '192.168.18.8', 'a5e0fef167323362', version=3.4)
windowRight = tinytuya.CoverDevice('bf1bcf4ed0e156e13bsbvz', '192.168.18.6', 'c6db31d029839f98', version=3.3)
windowLeft = tinytuya.CoverDevice('bf013c91d887adce65taat', '192.168.18.7', '651823889d72de81', version=3.3)

if __name__ == '__main__':
    app.run()


# Light requests
@app.route('/light/set/<int:status>')
def light_set(status):
    if status == 1:
        lightBulb.turn_on()
        return json.dumps({
            'success': True,
            'message': 'Light on'
        })

    else:
        lightBulb.turn_off()
        return json.dumps({
            'success': True,
            'message': 'Light off'
        })


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
            'message': 'Unknown code'
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


def get_side(data):
    if data == 'left':
        return windowLeft
    elif data == 'right':
        return windowRight
    else:
        return False
