install.packages("quadprog")
install.packages("PerformanceAnalytics")
install.packages("IntroCompFinR", repos="http://R-Forge.R-project.org")
library(IntroCompFinR)
library(tidyverse)

dados <- readxl::read_xlsx('APS 1 - PARTE1 - Robert Straub e Guilhermo Pastore.xlsx',
                           sheet = "RETORNO DOS ATIVOS DE RISCO")
#RETORNO DO ATIVO LIVRE DE RISCO
rf = 0.0067

#DATA FRAME DOS RETORNOS

ret_ativos_risco <- dados %>% 
  select(c(PETR4:WEG3))

#RETORNO MÉDIO
ret_medio <- rbind(mean(dados$PETR4),mean(dados$VALE3),mean(dados$GGBR3),mean(dados$SLCE3),mean(dados$CMIG3),mean(dados$ELET3),mean(dados$USIM3),mean(dados$BBDC4),
        mean(dados$BBAS3),mean(dados$ITUB4),mean(dados$SANB4),mean(dados$BOVA11),mean(dados$JBSS3),mean(dados$MGLU3),mean(dados$FLRY3),mean(dados$WEG3))
row.names(ret_medio) <- c("PETR4","VALE3","GGBR3","SLCE3","CMIG3","ELET3","USIM3","BBDC4","BBAS3","ITUB4","SANB4","BOVA11","JBSS3",
                          "MGLU3","FLRY3","WEG3")
colnames(ret_medio) <- c("Retornos")

#MATRIZ DE COVARIÂNCIA 
mat_covar <- cov(ret_ativos_risco)

#MATRIZ DE CORRELAÇÃO
mat_corr <- cor(ret_ativos_risco)

#CARTEIRA EFICIENTE
cart_ef <- tangency.portfolio(ret_medio,mat_covar,rf, shorts = F)
summary(cart_ef)

#CARTEIRADE MÍNIMA VARIÂNCIA 
cart_var_min <- globalMin.portfolio(ret_medio, mat_covar, shorts = F)
summary(cart_var_min)

#FRONTEIRA EFICIENTE
front_efic <- efficient.frontier(ret_medio, mat_covar, nport = 10000, shorts = F)


summary(front_efic)

#GRÁFICOS 
plot(front_efic, plot.assets = T, col="red", pch=20)

points(cart_var_min$sd, cart_var_min$er, col="blue", pch=10, cex=2)
points(cart_ef$sd,cart_ef$er, col="green", pch=10, cex=2)

text(cart_var_min$sd,cart_var_min$er, labels = "Risco Mínimo", pos=2)
text(cart_ef$sd,cart_ef$er, labels = "Carteira de Risco Ótima")

sharpe <- (cart_ef$er-rf)/cart_ef$sd
abline(a = rf, b = sharpe, col="green",lwd=2)

#PESOS ÓTIMOS PARA ALOCAÇÃO NO PORTIFÓLIO DE RISCO DADO A AVERSÃ AO RISCO

peso_agressivo = (cart_ef$er-rf)/(2*(cart_ef$sd^2))
peso_moderado = (cart_ef$er-rf)/(5*(cart_ef$sd^2))
peso_conservador = (cart_ef$er-rf)/(8*(cart_ef$sd^2))

tab_pesos <- tibble(peso_agressivo,peso_moderado,peso_conservador)
colnames(tab_pesos)=c("AGRESSIVO", "MODERADO","CONSERVADOR")
row.names(tab_pesos)=c("PESO NO PORTIFÓLIO DE RISCO")
