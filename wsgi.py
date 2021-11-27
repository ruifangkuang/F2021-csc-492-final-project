# NOTE: For more info on deploying to server, see this tutorial: https://dev.to/techparida/how-to-deploy-a-flask-app-on-heroku-heb

from main import app

if __name__ == "__main__":
  app.run(debug=True)