from flask_cors import CORS

cors = CORS(resources={r"/*": {"origins": "*"}}) #intancio e defino (/*, {origins: "*"})