Sub ObterArquivos_V4()

    ' Define as variáveis
    Dim path As String
    Dim filename As String
    Dim cell As Range
    Dim filelist As New Collection
    Dim file As Variant
    Dim fileExists As Boolean
    Dim destCell As Range
    Dim destRange As Range
    Dim indesejado_1 As String
    Dim indesejado_2 As String
    
    ' Define o caminho do arquivo a partir da célula J11
    path = Range("J11").Value
    
    ' Verifica se o caminho é válido
    If Dir(path, vbDirectory) = "" Then
        MsgBox "O caminho especificado não é válido."
        Exit Sub
    End If
    
    ' Percorre o diretório e adiciona os nomes dos arquivos à lista
    filename = Dir(path & "\*.*")
    Do While filename <> ""
        filelist.Add filename
        filename = Dir()
    Loop
    
    ' Verifica se existem arquivos com os mesmos nomes que as células J19 e J20
    indesejado_1 = Range("J19").Value
    indesejado_2 = Range("J20").Value
    
    ' Copia os arquivos que não têm os mesmos nomes especificados para a coluna R
    Set destCell = Range("A2")
    For Each file In filelist
        fileExists = False
        If file = indesejado_1 Or file = indesejado_2 Then
            fileExists = True
        End If
        If Not fileExists Then
            destCell.Value = file
            Set destCell = destCell.Offset(1)
        End If
    Next file
    
    ' Classifica a coluna R em ordem alfabética
    Set destRange = Range("A2").Resize(destCell.Row - 1 - Range("R2").Row + 1)
    destRange.Sort Key1:=destRange.Cells(1, 1), Order1:=xlAscending, Header:=xlNo
    
End Sub
