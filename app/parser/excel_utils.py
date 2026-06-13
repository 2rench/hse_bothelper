import xlrd

def get_merged_cell_value(sheet, row, col):

    for merged in sheet.merged_cells:

        row_start, row_end, col_start, col_end = merged

        if (
            row_start <= row < row_end
            and
            col_start <= col < col_end
        ):
            return sheet.cell_value(row_start, col_start)

    return None
