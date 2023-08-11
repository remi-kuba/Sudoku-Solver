from flask import Flask, render_template, request, jsonify
from main import Solver, Regrid, UnRegrid
import os

app = Flask(__name__)

dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(dir,"template")
app.template_folder = template_folder
app.static_folder = template_folder

# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    grid_values = request.json
    new_grid = Regrid(grid_values)
    solved = Solver(new_grid)
    print(*solved, sep='\n')
    solved = UnRegrid(solved)
    return jsonify(solved)

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
