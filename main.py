from api import create_app
import sensors.async_py as async_py
import threading

app = create_app()


def run_async():
    async_py.run()

if __name__ == '__main__':
    print("Running async_py.py")
    threading.Thread(target=run_async, daemon=True).start()

    print("Flask")
    print("Running the app")
    app.run(host='0.0.0.0', port=5000, debug = True)
    