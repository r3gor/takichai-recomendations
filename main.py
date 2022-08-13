# import src.scripts.upload_initial_data as uid
# uid.main()

from src.server.main import app

if __name__ == '__main__':
    app.run(debug=True)