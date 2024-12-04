import sys

def get_cell_value(file_path, row_num, col_num):
    try:
        table = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                row = line.strip().split(',')[0:-1]
                table.append(row)
            if(len(table) < row_num + 1):
                print(f"указана некорректная строка, в таблице {len(table)} строк")   
                return   
            if(len(table[row_num]) < col_num + 1):
                print(f"указан некорректный столбец, в таблице {len(table[row_num])} столбцов")
                return
        print(table[row_num][col_num])                   
    
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    if len(sys.argv) != 4:
        print("Некорректные аргументы, правильный порядок <file_path> <row_num> <row_num>")
    else:
        path = sys.argv[1]
        row_from_user = int(sys.argv[2])
        col_from_user = int(sys.argv[3])
        get_cell_value(path, row_from_user - 1, col_from_user - 1)


if __name__ == "__main__":
    main()