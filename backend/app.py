from backend import app
import backend.routes  # ต้องมีเพื่อให้ route ถูกโหลด

if __name__ == '__main__':
    app.run(debug=True)
