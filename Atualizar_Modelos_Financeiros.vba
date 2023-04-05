Sub AtualizarModeloFinanceiro_V4()
    
    Dim opcao As String
    
    opcao = InputBox("Quer atualizar todos os modelos financeiros ou quer fazer um teste primeiro para uma carteira?" & vbCrLf & vbCrLf & _
                     "--> Para atualizar todos os modelos: 'Atualizar tudo'" & vbCrLf & _
                     "--> Para realizar apenas um teste: 'Teste'")
    
    If opcao = "Atualizar tudo" Then
    
        
        Dim originalPath As String
        originalPath = Range("J11").Value
            
        
        Dim newPath As String
        newPath = Range("J14").Value
            
        Dim localizarStr As String
        Dim substituirStr As String
        localizarStr = Range("J5").Value
        substituirStr = Range("J8").Value
        
        Dim dataAtualizacao As Date
        dataAtualizacao = Range("J2").Value
            
        
        Dim FSO As Object
        Set FSO = CreateObject("Scripting.FileSystemObject")
            
        
        Dim i As Integer
        For i = 2 To Range("D" & Rows.Count).End(xlUp).Row
        
            On Error GoTo Trata_erro
            
                Dim originalName As String
                Dim newName As String
                originalName = Range("D" & i).Value
                newName = Range("F" & i).Value
                FSO.CopyFile originalPath & "\" & originalName, newPath & "\" & newName
                    
                
                If FSO.fileExists(newPath & "\" & newName) Then
                    
                    Dim wb As Workbook
                    Set wb = Workbooks.Open(newPath & "\" & newName)
                        
                    
                    Dim ws As Worksheet
                    Set ws = wb.Sheets("Calculo - P&L Compra")
                    ws.Activate
                        
                    ' Tarefa:
                        
                    Dim inserircol As Integer
                                      
                    Dim contaCol As Integer
                    contaCol = ws.Cells(33, Columns.Count).End(xlToLeft).Column
                        
                    Dim dataCol As Date
                    Dim dataColAnterior As Date
                    Dim dataColPosterior As Date
                    Dim verificaData As String
                        
                    verificaData = ws.Cells(33, 4)
                        
                    If verificaData >= dataAtualizacao Then
                        
                        wb.Close SaveChanges:=True
                        
                        Set wb = Nothing
                        Set ws = Nothing
                              
                        Range("G" & i) = "Arquivo atualizado com sucesso"
                        
                    
                    Else
                    
                        Dim j As Integer
                            
                        For j = 2 To contaCol
                            dataCol = ws.Cells(33, j).Value
                            dataColAnterior = ws.Cells(33, j - 1).Value
                            dataColPosterior = ws.Cells(33, j + 1).Value
                                
                            If dataColAnterior < dataAtualizacao And dataAtualizacao < dataColPosterior Then
                                inserircol = j
                                Exit For
                            End If
                        Next j
                            
                        If ws.Cells(36, inserircol - 1).Value < 0 Then
                            ws.Cells(33, inserircol) = "=FIMMÊS(" & ws.Cells(33, inserir - 1) & ";0)+1"
                            ws.Range(ws.Cells(34, inserircol - 1), ws.Cells(35, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(33, inserircol), ws.Cells(35, inserircol))
                                
                            ws.Cells(36, inserircol) = 0
                                
                            ws.Range(ws.Cells(37, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(37, inserircol), ws.Cells(71, inserircol))
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy
                            
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).PasteSpecial Paste:=xlPasteValues
                            
                            ws.Cells(33, inserircol - 1) = "mes_analise"
                            
                        Else
                            
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(33, inserircol), ws.Cells(71, inserircol))
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy
                            
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).PasteSpecial Paste:=xlPasteValues
                            
                        End If
                            
                        'ws.Cells(1, 10) = "Certo"
                            
                        Dim rng As Range
                        Dim celula As Range
                          
                        
                        Set rng = Range(Cells(35, inserircol), Cells(71, inserircol))
                        
                        
                        For Each celula In rng
                            If InStr(1, celula.Formula, localizarStr, vbTextCompare) > 0 Then
                                celula.Formula = Replace(celula.Formula, localizarStr, substituirStr, vbTextCompare)
                            End If
                        Next celula
                
                        Application.CutCopyMode = False
                            
                        
                        wb.Close SaveChanges:=True
                            
                        Set wb = Nothing
                        Set ws = Nothing
                              
                        Range("G" & i) = "Arquivo atualizado com sucesso"
                    End If
                
                Else
                    Debug.Print "Houve um erro ao copiar o arquivo "
                End If
            
        Next i
        
        Exit Sub
         
    ElseIf opcao = "Teste" Then
    
        originalPath = Range("J11").Value
            
        newPath = Range("J14").Value
            
        localizarStr = Range("J5").Value
        substituirStr = Range("J8").Value
            
        dataAtualizacao = Range("J2").Value
            
        Set FSO = CreateObject("Scripting.FileSystemObject")
            
        For i = 2 To 2
        
            On Error GoTo Trata_erro
            
                originalName = Range("D" & i).Value
                newName = Range("F" & i).Value
                FSO.CopyFile originalPath & "\" & originalName, newPath & "\" & newName
                    
            
                If FSO.fileExists(newPath & "\" & newName) Then

                    Set wb = Workbooks.Open(newPath & "\" & newName)
                        
                    Set ws = wb.Sheets("Calculo - P&L Compra")
                    ws.Activate
                        
                    ' Tarefa:
                        
                    contaCol = ws.Cells(33, Columns.Count).End(xlToLeft).Column
                        
                    verificaData = ws.Cells(33, 4)
                        
                    If verificaData >= dataAtualizacao Then
                        
                        wb.Close SaveChanges:=True
                        
                        Set wb = Nothing
                        Set ws = Nothing
                              
                        Range("G" & i) = "Arquivo atualizado com sucesso"
                        
                    
                    Else

                        For j = 2 To contaCol
                            dataCol = ws.Cells(33, j).Value
                            dataColAnterior = ws.Cells(33, j - 1).Value
                            dataColPosterior = ws.Cells(33, j + 1).Value
                                
                            If dataColAnterior < dataAtualizacao And dataAtualizacao < dataColPosterior Then
                                inserircol = j
                                Exit For
                            End If
                        Next j
                            
                        If ws.Cells(36, inserircol - 1).Value < 0 Then
                            ws.Cells(33, inserircol) = "=FIMMÊS(" & ws.Cells(33, inserir - 1) & ";0)+1"
                            ws.Range(ws.Cells(34, inserircol - 1), ws.Cells(35, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(33, inserircol), ws.Cells(35, inserircol))
                                
                            ws.Cells(36, inserircol) = 0
                                
                            ws.Range(ws.Cells(37, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(37, inserircol), ws.Cells(71, inserircol))
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy
                            
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).PasteSpecial Paste:=xlPasteValues
                            
                            ws.Cells(33, inserircol - 1) = "mes_analise"
                            
                        Else
                            
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy _
                                Destination:=ws.Range(ws.Cells(33, inserircol), ws.Cells(71, inserircol))
                                
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).Copy
                            
                            ws.Range(ws.Cells(33, inserircol - 1), ws.Cells(71, inserircol - 1)).PasteSpecial Paste:=xlPasteValues
                            
                        End If
                            
                        'ws.Cells(1, 10) = "Certo"
    
                        Set rng = Range(Cells(35, inserircol), Cells(71, inserircol))
                        
                        
                        For Each celula In rng
                            If InStr(1, celula.Formula, localizarStr, vbTextCompare) > 0 Then
                                celula.Formula = Replace(celula.Formula, localizarStr, substituirStr, vbTextCompare)
                            End If
                        Next celula
                
                        Application.CutCopyMode = False
                            
                        
                        wb.Close SaveChanges:=True
                            
                        
                        Set wb = Nothing
                        Set ws = Nothing
                          
                        Range("G" & i) = "Arquivo atualizado com sucesso"
                    
                    End If
                    
                Else
                    Debug.Print "Houve um erro ao copiar o arquivo "
                End If
            
        Next i
        
        Exit Sub
        
Trata_erro:
        
        Dim Ponto_de_resumo As Integer
        Dim dado As Range
        
        Ponto_de_resumo = 1
        
        For Each dado In Range("G2:G" & Cells(Rows.Count, "G").End(xlUp).Row)

            If InStr(1, dado.Value, "Arquivo atualizado com sucesso", vbTextCompare) > 0 Then

                Ponto_de_resumo = Ponto_de_resumo + 1
            End If
        Next dado
        
        Range("G" & Ponto_de_resumo + 1) = "Erro ao atualizar o arquivo"
    
        Dim Resposta As String
        
        Mensagem = MsgBox("Erro: " & Err.Description & vbCrLf)
        
        Resposta = InputBox("Quer continuar o código no próximo arquivo?")
        
        If Resposta = "Sim" Or Resposta = "sim" Then
            i = Ponto_de_resumo + 1
            Resume Next
        Else
            Exit Sub
        End If
    
    End If
End Sub
