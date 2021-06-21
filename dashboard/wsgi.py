from app import server as application

if __name__ == '__main__':
    application.run(port=80, host='0.0.0.0')