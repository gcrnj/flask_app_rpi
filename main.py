from api import create_app
import async_py
import threading

app = create_app()


def run_async():
    async_py.run()

if __name__ == '__main__':
    print("Running async_py.py")
    threading.Thread(target=run_async, daemon=True).start()

    print("Flask")
    app.run(host='0.0.0.0', port=5000, debug = True)
    