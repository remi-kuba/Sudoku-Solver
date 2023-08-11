const container = document.getElementById('sudoku-container');

function createCell(row, col) {
  const cell = document.createElement('input');
  cell.type = 'text';
  cell.className = 'cell';
  cell.dataset.row = row;
  cell.dataset.col = col;
  return cell;
}

document.getElementById('submit-button').addEventListener('click', function () {
    solveSudoku();
});

function getGridValues() {
  const gridValues = [];
  const cells = document.querySelectorAll('.cell');
  cells.forEach(function (cell) {
    gridValues.push(cell.value);
  });
  return gridValues;
}

function solveSudoku() {
    const gridValues = getGridValues();
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/solve', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const solvedValues = JSON.parse(xhr.responseText);
        updateGridWithSolvedValues(solvedValues);
      }
    };
    xhr.send(JSON.stringify(gridValues));
}


function updateGridWithSolvedValues(solvedValues) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(function (cell, index) {
      cell.value = solvedValues[index];
    });
}


function generateGrid() {
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = createCell(row, col);
      container.appendChild(cell);
    }
  }
}

generateGrid();
