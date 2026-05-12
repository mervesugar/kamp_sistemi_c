#include "structures.h"
#include "common.h"
// 10. MATRIX 2D
// ---------------------------------------------------------
EXPORT Matrix2D* matrix_create(int rows, int cols, int default_val) {
    if (rows <= 0 || cols <= 0) return NULL;
    Matrix2D *m = malloc(sizeof(Matrix2D));
    if (m) {
        m->rows = rows;
        m->cols = cols;
        m->data = malloc(sizeof(int) * rows * cols);
        for(int i=0; i<rows*cols; i++) m->data[i] = default_val;
    }
    return m;
}

EXPORT void matrix_set(Matrix2D *m, int row, int col, int value) {
    if (m && row >= 0 && row < m->rows && col >= 0 && col < m->cols) {
        m->data[row * m->cols + col] = value;
    }
}

EXPORT int matrix_get(Matrix2D *m, int row, int col) {
    if (m && row >= 0 && row < m->rows && col >= 0 && col < m->cols) {
        return m->data[row * m->cols + col];
    }
    return 0;
}

EXPORT void matrix_increment(Matrix2D *m, int row, int col, int amount) {
    if (m && row >= 0 && row < m->rows && col >= 0 && col < m->cols) {
        m->data[row * m->cols + col] += amount;
    }
}

EXPORT int matrix_row_sum(Matrix2D *m, int row) {
    if (!m || row < 0 || row >= m->rows) return 0;
    int sum = 0;
    for(int c=0; c<m->cols; c++) sum += m->data[row * m->cols + c];
    return sum;
}

EXPORT int matrix_col_sum(Matrix2D *m, int col) {
    if (!m || col < 0 || col >= m->cols) return 0;
    int sum = 0;
    for(int r=0; r<m->rows; r++) sum += m->data[r * m->cols + col];
    return sum;
}

EXPORT void matrix_destroy(Matrix2D *m) {
    if (m) { free(m->data); free(m); }
}

// ---------------------------------------------------------
