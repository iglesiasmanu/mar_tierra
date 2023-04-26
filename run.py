from mar_tierra import Config, create_app
import os

try:
    ENV = os.environ['ENV']
except:
    ENV = 'DEV'

#app, socketio = create_app()

#if __name__ == '__main__':
#    socketio.run(app, host='0.0.0.0', debug=True, port=8080) if ENV == 'PROD' else app.run(host='0.0.0.0', debug=True)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080) if ENV == 'PROD' else app.run(host='0.0.0.0', debug=True)

