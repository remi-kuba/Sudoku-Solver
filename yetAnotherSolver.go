package main 
import("fmt")

func Valid(board [][]int, row, col int) []int {
	already := make([]int,0)
	res := make([]int, 0)
	for _, i := range board[row] {
		already = append(already,i)
	}
	for r := 0; r < 9; r++ {
		already = append(already,board[r][col])
	}
	for r := row/3*3; r < row/3*3+3; r++ {
		for c := col/3*3; c < col/3*3+3; c++ {
			already = append(already,board[r][c])
		}
	}
	for i := 1; i <= 9; i++ {
		if !InList(already,i) {
			res = append(res,i)
		}
	}
	return res 
}

func InList(list []int, number int) bool {
	for _, i := range list {
		if i == number {
			return true 
		}
	}
	return false
}


func Solver(board [][]int) [][]int {
	dim := 9
	for row := 0; row < dim; row++ {
		for col := 0; col < dim; col++ {
			if board[row][col] != 0 {
				continue
			}
			for _, val := range Valid(board,row,col) {
				board[row][col] = val 
				result := Solver(board)
				if result != nil {
					return result 
				}
			}
			board[row][col] = 0
			return nil 
		}
	}
	return board 
}
