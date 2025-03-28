from app import create_app
#from app.app import app as flask_app
from playground import app as playground_app
app = create_app()  
    
if __name__== "__main__":
        app.run(debug=True)

