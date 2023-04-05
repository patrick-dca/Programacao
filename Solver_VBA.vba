Sub Tabela_de_TIR()
    Dim numbers As Variant
    numbers = Array(0.275, 0.3, 0.325, 0.35, 0.375, 0.4) ' Lista de números para o loop

    For i = LBound(numbers) To UBound(numbers)
        'Cells(5, 1) = numbers(i) Muda o valor da célula A5
        SolverOk SetCell:=Range("F12"), MaxMinVal:=3, ValueOf:=numbers(i), ByChange:=Range("C49"), _
            Engine:=1, EngineDesc:="GRG Nonlinear"
        SolverSolve (True)
        Cells(55 + i, 5) = Range("F12").Value ' Cola o input na coluna C
        Cells(55 + i, 6) = Range("C49").Value ' Cola o output na coluna D
    Next i
End Sub
