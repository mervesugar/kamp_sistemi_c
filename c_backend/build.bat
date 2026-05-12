@echo off
set PATH=C:\msys64\mingw64\bin;%PATH%
echo ============================================================
echo  BMT210 Veri Yapilari - C Backend Derleme Betigi
echo  11 Veri Yapisi ayri dosyalardan derleniyor...
echo ============================================================
echo.

echo [1/11] common.c         - Ortak yardimci fonksiyonlar
echo [2/11] linkedlist.c     - Bagli Liste (Linked List)
echo [3/11] stack.c          - Yigin (Stack)
echo [4/11] queue.c          - Kuyruk (Queue)
echo [5/11] campset.c        - Kume (Set)
echo [6/11] hashmap.c        - Hash Tablosu (Hash Map)
echo [7/11] bst.c            - Ikili Arama Agaci (BST)
echo [8/11] priority_queue.c - Oncelikli Kuyruk (Priority Queue)
echo [9/11] maxheap.c        - Maksimum Yigin (Max Heap)
echo [10/11] graph.c         - Graf (Graph + Dijkstra)
echo [11/11] matrix2d.c      - 2D Matris (Matrix)
echo [+]    camptree.c       - Kamp Agaci (N-ary Tree)
echo.

gcc -shared -o structures.dll ^
    common.c ^
    linkedlist.c ^
    stack.c ^
    queue.c ^
    campset.c ^
    hashmap.c ^
    bst.c ^
    priority_queue.c ^
    maxheap.c ^
    graph.c ^
    matrix2d.c ^
    camptree.c

if %errorlevel% neq 0 (
    echo.
    echo [HATA] Derleme BASARISIZ! MinGW GCC kurulu oldugundan emin olun.
    pause
    exit /b %errorlevel%
)

echo.
echo [BASARILI] structures.dll olusturuldu!
echo            Toplam: 12 C dosyasi -^> 1 DLL
pause
